CATEGORY = "RapSheet-Inspired Correlated"

# Input data will be of the following form:
# {
#       "data": [<list of alerts>],
#       "tp_count": 123,
#       "fp_count": 456,
# }
#
# Each category (and its data) will be displayed separately in each graph


class SeverityScore:
    title = "Severity Score"
    description = """
    Assign a risk score according to the SRE severity value.
    """

    required_fields = [
        "event.severity",
    ]

    default_param1 = 123
    default_param2 = "qwer"

    @staticmethod
    def process_data(data):
        data["tp_count"] = data["tp_count"] + 10
        data["fp_count"] = data["fp_count"] - 10
        return data


class ConfidenceModifier:
    title = "Confidence Modifier"
    description = """
    Modifies the value according to the SRE confidence score.
    """

    required_fields = [
        "event.confidence",
    ]

    default_param1 = 456
    default_param2 = "qwer"

    @staticmethod
    def process_data(data):
        data["tp_count"] = data["tp_count"] - 20
        data["fp_count"] = data["fp_count"] + 20
        return data


class LongestTacticsPath:
    title = "Longest Tactics Path"
    description = """
    Correlates SRE by finding longest paths through ATT&CK tactics per host
    """

    required_fields = [
        "@timestamp",
        "attack.technique",
        "attack.tactic",
        "host.name",
    ]

    default_param1 = 789
    default_param2 = "qwer"

    @staticmethod
    def process_data(data):
        data["tp_count"] = data["tp_count"] * 0.8
        data["fp_count"] = data["fp_count"] * 0.8
        return data
