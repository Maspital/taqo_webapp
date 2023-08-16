import re


class SuricataScore:
    title = "Suricata Score"
    id = "594055f8c8588c9c19c2e4f11bdf8c78"
    description = """
    Assigns a risk score based on the suricata "priority" value, if it exists.
    """

    required_fields = ["event.message"]

    @staticmethod
    def process_data(dataset: dict) -> dict[dict]:
        events = dataset["data"]
        for index, sre in enumerate(events):
            new_score = SuricataScore.set_suricata_risk_score(sre)

            if new_score is None:
                continue    # keep old score

            sre.setdefault("event", {})
            sre["event"].setdefault("event", {})
            sre["event"]["event"]["risk_score"] = new_score
            sre["event"]["event"]["base_score"] = new_score
            events[index] = sre

        dataset["data"] = events
        return dataset

    @staticmethod
    def set_suricata_risk_score(sre: dict):
        pattern = r'\[Priority: (\d+)\]'
        match = re.search(pattern, sre["event"]["message"])
        if match:
            priority = int(match.group(1))
        else:
            return None

        max_score = 100
        if priority == 1:
            return max_score
        elif priority == 2:
            return int(0.75 * max_score)
        elif priority == 3:
            return int(0.5 * max_score)
        elif priority == 4:
            return int(0.25 * max_score)
        else:
            return 1
