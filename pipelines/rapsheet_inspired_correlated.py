CATEGORY = "RapSheet-Inspired Correlated"


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

    def process_data(self, data):
        print(self.default_param1)
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

    def process_data(self, data):
        print(self.default_param1)
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

    def process_data(self, data):
        print(self.default_param1)
        return data
