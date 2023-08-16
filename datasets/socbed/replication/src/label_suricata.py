import argparse
import json
import re
from pprint import pprint

from helper import extend_filename, save_labeled_dataset, apply_label_to_event

MSG_REGEX = re.compile(r"\[.*\] (.*) \[.*\] \[.*\] .*")


def main():
    args = parse_args()
    label_suricata(args.logfile)


def parse_args():
    parser = argparse.ArgumentParser(description='Count and label true positives for Suricata alerts')
    parser.add_argument("logfile", help='Single JSONL log file containing sysmon logs to label')
    return parser.parse_args()


def label_suricata(sim_id):
    with open(sim_id) as json_file:
        logfile = [json.loads(line) for line in json_file]

    logfile = label_events(logfile)
    save_labeled_dataset(data=logfile,
                         new_filename=extend_filename(sim_id, "LABELED", ".jsonl"))


def label_events(logfile):
    tp_counts = {}
    fp_counts = {}
    result = []

    for event in logfile:
        rule = get_msg_field(event)

        if not rule or "ET " not in rule:
            continue
        if is_true_positive(rule):
            tp_counts[rule] = tp_counts.get(rule, 0) + 1
            apply_label_to_event(event, True)
        else:
            fp_counts[rule] = fp_counts.get(rule, 0) + 1
            apply_label_to_event(event, False)
        event["rule"] = rule
        normalize_json(event)
        result.append(event)

    sort_by_timestamp(result)
    print_results(tp_counts, fp_counts)
    return result


def get_msg_field(event):
    if "program" in event and event["program"] == "suricata":
        try:
            rule = MSG_REGEX.search(event["message"]).group(1)
            return rule
        except AttributeError:
            print(f"\033[93m[WARNING]\033[0m Skipping Suricata message: {event['message'].strip()}")
            return event['message'].strip()


def normalize_json(event):
    event_fields = ["@timestamp", "@version", "facility", "facility_label", "host", "logsource", "message", "pid",
                    "priority", "program", "severity", "severity_label", "timestamp", "timestamp8601", "type"]
    rule_fields = ["rule"]
    metadata_fields = ["misuse"]

    event["event"] = {}
    for field in event_fields:
        try:
            event["event"][field] = event.pop(field)
        except KeyError:
            print(f"\033[94m[INFO]\033[0m Expected event field \"{field}\" is not present.")

    event["rule"] = {}
    for field in rule_fields:
        try:
            event["rule"][field] = event.pop(field)
        except KeyError:
            print(f"\033[94m[INFO]\033[0m Expected rule field \"{field}\" is not present.")

    event["metadata"] = {}
    for field in metadata_fields:
        try:
            event["metadata"][field] = event.pop(field)
        except KeyError:
            print(f"\033[94m[INFO]\033[0m Expected metadata field \"{field}\" is not present.")


def sort_by_timestamp(list_of_dicts):
    list_of_dicts.sort(key=lambda item: item["event"]["@timestamp"])


def is_true_positive(rule):
    tps = {
        # misc_sqlmap
        'ET SCAN Sqlmap SQL Injection Scan',
        'ET WEB_SERVER Possible SQL Injection Attempt SELECT FROM',
        'ET WEB_SERVER Possible SQL Injection Attempt UNION SELECT',
        'ET WEB_SERVER Script tag in URI Possible Cross Site Scripting Attempt',
        'ET WEB_SERVER Attempt To Access MSSQL xp_cmdshell Stored Procedure Via URI',
        'ET WEB_SERVER Possible MySQL SQLi Attempt Information Schema Access',
        'ET WEB_SERVER SQL Errors in HTTP 200 Response (error in your SQL syntax)',
        'ET WEB_SERVER MYSQL SELECT CONCAT SQL Injection Attempt',
        'ET WEB_SERVER SQL Injection Select Sleep Time Delay',
        'ET WEB_SERVER MYSQL Benchmark Command in URI to Consume Server Resources',
        'ET WEB_SERVER Possible Attempt to Get SQL Server Version in URI using SELECT VERSION',
        'ET WEB_SERVER Possible attempt to enumerate MS SQL Server version',
        'ET WEB_SERVER ATTACKER SQLi - SELECT and Schema Columns',
        # infect_email_exe
        'ET INFO SUSPICIOUS SMTP EXE - EXE SMTP Attachment',
        # c2_take_screenshot
        'ET POLICY PE EXE or DLL Windows file download HTTP',
        'ET INFO Executable Retrieved With Minimal HTTP Headers - Potential Second Stage Download',
        'ET INFO SUSPICIOUS Dotted Quad Host MZ Response',
        'ET INFO EXE IsDebuggerPresent (Used in Malware Anti-Debugging)',
        'ET TROJAN Possible Metasploit Payload Common Construct Bind_API (from server)',
        # c2_exfiltration
        # c2_mimikatz
        # misc_download_malware
        'ET INFO Executable Download from dotted-quad Host',
        'ET POLICY PE EXE or DLL Windows file download HTTP',  # duplicate
        'ET INFO SUSPICIOUS Dotted Quad Host MZ Response',  # duplicate
        # misc_set_autostart
        # misc_execute_malware
    }
    if rule in tps:
        return True
    return False


def print_results(tp_counts, fp_counts):
    print("Rule hits (true positives):")
    pprint(tp_counts)
    print("Rule hits (false positives):")
    pprint(fp_counts)


if __name__ == '__main__':
    main()
