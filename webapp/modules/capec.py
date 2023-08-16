from src.module_src import capec_score


class CapecScore:
    title = "Capec Score"
    id = "260dbe1d7613bc849c59ca6c8d4bfb8c"
    description = """
    Adds a score derived from the CAPEC knowledge base, if such an entry exists.
    """

    required_fields = [
        "rule.tags",
        "CAPEC score for given technique"
    ]

    custom_params = {
        "Severity Weight": {
            "type": "SINGLE_NUMBER",
            "default": 2,
            "min": 1,
            "max": 10,
            "step": 1,
        },
        "Likelihood Weight": {
            "type": "SINGLE_NUMBER",
            "default": 1,
            "min": 1,
            "max": 10,
            "step": 1,
        },
        "Behavior for multiple CAPEC scores": {
            "type": "RADIO",
            "default": "highest",
            "options": {"highest": "Highest Score", "mean": "Arithmetic Mean"},
        },
    }

    @staticmethod
    def process_data(data, params):
        severity_weight = params["Severity Weight"]
        likelihood_weight = params["Likelihood Weight"]
        mult_score_handling = params["Behavior for multiple CAPEC scores"]
        data = capec_score.process(
            data,
            mult_score_handling,
            severity_weight=severity_weight,
            likelihood_weight=likelihood_weight
        )
        return data
