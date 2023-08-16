from math import prod
import re

from src.module_src.exceptions import InvalidSequenceMember


TACTICS = [
        "reconnaissance",
        "resource_development",
        "initial_access",
        "execution",
        "persistence",
        "privilege_escalation",
        "defense_evasion",
        "credential_access",
        "discovery",
        "lateral_movement",
        "collection",
        "command_and_control",
        "exfiltration",
        "impact",
    ]


def find_tactic_from_alert(cur_alert: dict) -> list[int]:
    try:
        tags = cur_alert["rule"]["tags"]
    except KeyError:
        raise InvalidSequenceMember

    all_tactics = TACTICS
    found_tactics = []
    for tag in tags:
        tactic = tag.split(".")[1]
        if tactic in all_tactics:
            found_tactics.append(all_tactics.index(tactic))

    if not found_tactics:
        raise InvalidSequenceMember
    found_tactics.sort()
    return found_tactics


def validate_legal_tactic(cur_tactic: int, new_tactic: int, dup_setting: str) -> bool:
    if dup_setting == "no_dup_tactics":
        return new_tactic > cur_tactic
    else:
        return new_tactic >= cur_tactic


def find_techniques_from_alert(cur_alert: dict) -> list[str]:
    # matches t1234 or t1234.123
    pattern = r"t\d{4}(\.\d{3})?"
    all_techniques = []

    try:
        tags = cur_alert["rule"]["tags"]
    except KeyError:
        raise InvalidSequenceMember

    for tag in tags:
        # tags look like this:
        # attack.execution or attack.t1234
        technique = tag.split(".")[1]
        if re.match(pattern, technique):
            all_techniques.append(technique)
    return all_techniques


def validate_legal_techniques(cur_techs: list[str], new_techs: list[str], dup_setting: str) -> bool:
    if dup_setting == "no_dup_techniques":
        # check if there are any common techniques
        return not bool(set(cur_techs) & set(new_techs))
    else:
        return True


def find_rule_from_alert(cur_alert: dict) -> str:
    try:
        rule_name = cur_alert["rule"]["name"]
    except KeyError:
        raise InvalidSequenceMember
    return rule_name


def validate_legal_rule(cur_rule: str, new_rule: str, dup_setting: str) -> bool:
    if dup_setting == "no_dup_rules":
        return cur_rule != new_rule
    else:
        return True


def find_hostname_from_alert(cur_alert: dict) -> str:
    try:
        hostname = cur_alert["event"]["agent"]["hostname"]
    except KeyError:
        raise InvalidSequenceMember
    return hostname


def validate_same_host(starting_hostname: str, new_hostname: str) -> None:
    if new_hostname != starting_hostname:
        raise InvalidSequenceMember


def find_process_info_from_alert(cur_alert: dict) -> (int, int):
    cur_pid = cur_parent = None
    try:
        cur_pid = cur_alert["event"]["process"]["pid"]
    except KeyError:
        pass
    try:
        cur_parent = cur_alert["event"]["process"]["parent"]["pid"]
    except KeyError:
        pass

    if cur_pid is None and cur_parent is None:
        raise InvalidSequenceMember
    return cur_pid, cur_parent


def validate_same_process_origin(allowed_pids: list[int], new_pid: int, new_parent: int) -> list[int]:
    if new_pid in allowed_pids or new_parent in allowed_pids:
        pass
    else:
        raise InvalidSequenceMember


def calculate_score(all_alerts: list, sequence: list[int], comp_method: str) -> int:
    scores = []
    for index in sequence:
        scores.append(all_alerts[index]["event"]["event"]["base_score"])

    if comp_method == "addition":
        return sum(scores)
    elif comp_method == "multiplication":
        return prod(scores)


def assign_score_to_alerts(all_alerts: list, sequence: list[int], new_score: int) -> list:
    for index in sequence:
        old_score = all_alerts[index]["event"]["event"]["risk_score"]
        if new_score > old_score:
            all_alerts[index]["event"]["event"]["risk_score"] = new_score
    return all_alerts
