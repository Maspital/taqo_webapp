class Baseline:
    title = "Baseline"
    id = "957701d5f667424187e32b97aa76f856"
    description = """
    Assign the same score to each SRE.
    """

    required_fields = []

    custom_params = {
        "Risk Score": {
            "type": "SINGLE_NUMBER",
            "default": 50,
            "min": 0,
            "max": 100,
            "step": 1,
        },
    }

    @staticmethod
    def process_data(dataset: dict, params) -> dict:
        score = params["Risk Score"]

        for index in range(len(dataset["data"])):
            dataset["data"][index]["event"].setdefault("event", {})
            dataset["data"][index]["event"]["event"]["risk_score"] = score
            dataset["data"][index]["event"]["event"]["base_score"] = score

        return dataset
