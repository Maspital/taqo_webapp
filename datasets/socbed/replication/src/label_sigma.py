import argparse
import json
from pprint import pprint
import re

from helper import extend_filename, save_labeled_dataset, apply_label_to_event

unknown_alerts = []


def main():
    args = parse_args()
    label_sigma(args.logfile, args.rules_dict)


def parse_args():
    parser = argparse.ArgumentParser(description='Count and label true positives for Sigma alerts')
    parser.add_argument("logfile", help='Single JSON log file containing Sigma alerts to label')
    parser.add_argument("rules_dict", help="dictionary containing rules for labeling")
    return parser.parse_args()


def label_sigma(sim_id, rules_dict):
    logfile, rules_dict = open_json_files(sim_id, rules_dict)

    label_alerts(logfile, rules_dict)
    save_labeled_dataset(data=logfile,
                         new_filename=extend_filename(sim_id, "LABELED", ".jsonl"))


def label_alerts(logfile, rules_dict):
    tp_counts = {}
    fp_counts = {}

    for sigma_alert in logfile:
        rule = sigma_alert["name"]
        if is_true_positive(sigma_alert, rule, rules_dict):
            tp_counts[rule] = tp_counts.get(rule, 0) + 1
            apply_label_to_event(sigma_alert, True)
        else:
            fp_counts[rule] = fp_counts.get(rule, 0) + 1
            apply_label_to_event(sigma_alert, False)
        normalize_json(sigma_alert)

    print_results(tp_counts, fp_counts)


def is_true_positive(sigma_alert, rule, rules_dict):
    target_rule_content = {}

    # there are certainly more efficient ways to do this, but runtime is still fairly short, so ¯\_(ツ)_/¯
    for rule_name, content in rules_dict.items():
        if rule_name == rule:
            target_rule_content = content
            break

    if not target_rule_content:
        if rule not in unknown_alerts:
            print(f"\033[93m[WARNING]\033[0m Unknown alert: {rule}")
            unknown_alerts.append(rule)
        return False

    conditions = target_rule_content["conditions"].values()
    label = len(conditions) > 0 and any(condition_is_met(sigma_alert, con) for con in conditions)

    return label


def condition_is_met(sigma_alert, condition):
    # NOTE: assumes key name itself NEVER contains a dot (.)
    relevant_dict_entry = condition[0].split(".")
    desired_content = re.compile(condition[1])
    actual_content = sigma_alert

    # iterate into the dict structure
    for key in relevant_dict_entry:
        try:
            actual_content = actual_content.get(key)
            # Some entries may come as lists. If that's the case, we only want the first entry to proceed
            if isinstance(actual_content, list):
                actual_content = actual_content[0]
        except AttributeError:
            return False

    return desired_content.match(actual_content)


def normalize_json(sigma_alert):
    rule_fields = ["name", "authors", "level", "status",
                   "falsepositives", "id", "logsource", "references", "tags"]
    metadata_fields = ["group", "source", "kind", "document", "timestamp", "misuse"]

    if "document" in sigma_alert:
        sigma_alert["event"] = sigma_alert["document"].pop("data")
    elif "documents" in sigma_alert:
        sigma_alert["document"] = sigma_alert["documents"][0]
        sigma_alert.pop("documents", None)
        sigma_alert["event"] = sigma_alert["document"].pop("data")
    else:
        print(f"\033[91m[ERROR]\033[0m Document field not present in alert!")

    sigma_alert["rule"] = {}
    for field in rule_fields:
        try:
            sigma_alert["rule"][field] = sigma_alert.pop(field)
        except KeyError:
            # print(f"\033[94m[INFO]\033[0m Expected rule field \"{field}\" is not present.")
            pass

    sigma_alert["metadata"] = {}
    for field in metadata_fields:
        try:
            sigma_alert["metadata"][field] = sigma_alert.pop(field)
        except KeyError:
            print(f"\033[93m[WARNING]\033[0m Expected metadata field \"{field}\" is not present.")

    # Rename certain fields
    sigma_alert["rule"]["title"] = sigma_alert["rule"].pop("name")


def open_json_files(logfile, rules_dict):
    with open(logfile) as json_file:
        json_data = json.load(json_file)

    with open(rules_dict) as json_file:
        json_rules = json.load(json_file)

    return json_data, json_rules


def print_results(tp_counts, fp_counts):
    print("Rule hits (true positives):")
    pprint(tp_counts)
    print("Rule hits (false positives):")
    pprint(fp_counts)


if __name__ == '__main__':
    main()
