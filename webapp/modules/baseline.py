class Baseline:
    title = "Baseline"
    id = "957701d5f667424187e32b97aa76f856"
    description = """
    Assign a risk score of 1 to each SRE.
    """

    required_fields = []

    custom_params = {}

    @staticmethod
    def process_data(dataset: dict) -> dict:
        for sre in dataset["data"]:
            try:
                Baseline.set_sigma_risk_score(sre)
            except KeyError:
                Baseline.set_suricata_risk_score(sre)

        return dataset

    @staticmethod
    def set_sigma_risk_score(sre: dict):
        sre["event"]["event"]["risk_score"] = 1

    @staticmethod
    def set_suricata_risk_score(sre: dict):
        sre["event"].setdefault("event", {})
        sre["event"]["event"]["risk_score"] = 1
