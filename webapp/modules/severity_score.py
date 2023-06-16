class SeverityScore:
    title = "Severity Score"
    id = "594055f8c8588c9c19c2e4f11bdf8c78"
    description = """
    Assign a risk score according to the SRE severity value.
    """

    required_fields = []

    custom_params = {
        "severity_mapping": {
            "type": "JSON",
            "label": "severity_mapping",
            "description": "Severity mapping that should be applied to the events",
            "default": '{"critical": 0, "high": 1, "medium": 2, "low": 3, "informational": 4}',
            "error_msg": "Incorrect JSON",
            "placeholder": "Severity mapping goes here",
        }
    }

    @staticmethod
    def process_data(dataset: dict, params: dict) -> dict[dict]:
        severity_mapping = params["severity_mapping"]

        for sre in dataset["data"]:
            try:
                SeverityScore.set_sigma_risk_score(sre, severity_mapping)
            except KeyError:
                SeverityScore.set_suricata_risk_score(sre)

        return dataset

    @staticmethod
    def set_sigma_risk_score(sre: dict, severity_mapping: dict):
        sre["event"]["event"]["risk_score"] = severity_mapping[sre["rule"]["level"]]

    @staticmethod
    def set_suricata_risk_score(sre: dict):
        # Does this always work? Maybe use a regex group to catch the priority value?
        priority = sre["event"]["message"].split("[")[3].split("]")[0].split()[1]
        assert float(priority) in range(1, 255 + 1)

        sre["event"].setdefault("event", {})
        sre["event"]["event"]["risk_score"] = int(priority)
