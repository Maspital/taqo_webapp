from dateutil.parser import parse

from src.module_src.exceptions import InvalidSequenceMember
import src.module_src.correlation as cor


class TimeCorrelation:
    title = "TTP/Timestamp Threat Score"
    id = "a7ea6936c4ad59be2bbaff4f17ac80ee"
    description = """
    Assigns a threat score based on observed TTPs and timestamps.
    """

    required_fields = ["rule.tags", "Pre-assigned base score"]

    custom_params = {
        "Maximum time Δ in minutes": {
            "type": "SINGLE_NUMBER",
            "default": 10,
            "min": 1,
            "max": 120,
            "step": 1,
        },
        "Computation within sequence": {
            "type": "RADIO",
            "default": "addition",
            "options": {"addition": "Addition", "multiplication": "Multiplication"},
        },
        "Rule for duplicates": {
            "type": "RADIO",
            "default": "allow_all",
            "options": {"allow_all": "Allow all",
                        "no_dup_techniques": "No duplicate techniques",
                        "no_dup_tactics": "No duplicate tactics",
                        "no_dup_rules": "No duplicate rules"},
        },
    }

    @staticmethod
    def process_data(dataset: dict, params: dict) -> dict[dict]:
        comp_method = params["Computation within sequence"]
        max_delta = params["Maximum time Δ in minutes"] * 60
        dup_setting = params["Rule for duplicates"]
        all_alerts = dataset["data"]

        for index, alert in enumerate(all_alerts):
            # obtain longest sequence
            try:
                sequence = TimeCorrelation.find_longest_sequence(max_delta, all_alerts, index, dup_setting)
            except InvalidSequenceMember:
                # raised if starting point is invalid or length of sequence is 1
                continue
            threat_score = cor.calculate_score(all_alerts, sequence, comp_method)
            all_alerts = cor.assign_score_to_alerts(all_alerts, sequence, threat_score)

        return dataset

    @staticmethod
    def find_longest_sequence(max_delta: int, all_alerts: list, index: int, dup_setting: str) -> list[int]:
        num_of_alerts = len(all_alerts)
        found_sequence = []

        cur_alert = all_alerts[index]
        cur_timestamp = parse(cur_alert["event"]["@timestamp"])
        cur_tactic = min(cor.find_tactic_from_alert(cur_alert))
        cur_techniques = cor.find_techniques_from_alert(cur_alert)
        cur_rule = cor.find_rule_from_alert(cur_alert)

        while index < num_of_alerts - 1:
            index += 1
            new_alert = all_alerts[index]
            new_timestamp = parse(new_alert["event"]["@timestamp"])

            if abs(new_timestamp - cur_timestamp).total_seconds() > max_delta:
                # maximum time difference overstepped, so we stop the entire sequence
                break

            try:
                new_tactics = cor.find_tactic_from_alert(new_alert)
                new_techniques = cor.find_techniques_from_alert(new_alert)
                new_rule = cor.find_rule_from_alert(new_alert)
            except InvalidSequenceMember:
                continue

            for new_tactic in new_tactics:
                # "If our new tactic is the same or comes later in the att&ck matrix"
                # "new_tactics" is ordered, so this will always get the smallest possible integer
                if cor.validate_legal_tactic(cur_tactic, new_tactic, dup_setting) and \
                        cor.validate_legal_techniques(cur_techniques, new_techniques, dup_setting) and \
                        cor.validate_legal_rule(cur_rule, new_rule, dup_setting):
                    found_sequence.append(index)
                    cur_timestamp = new_timestamp
                    cur_tactic = new_tactic
                    cur_techniques = new_techniques
                    cur_rule = new_rule
                    break

        if len(found_sequence) < 2:
            raise InvalidSequenceMember
        return found_sequence
