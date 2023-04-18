CATEGORY = "Trivial Uncorrelated"


class SeverityScore:
    title = "Severity Score"
    description = """
    Assign a risk score according to the SRE severity value.
    """

    required_fields = [
        "event.severity",
    ]

    default_param1 = 000
    default_param2 = "qwer"

    @staticmethod
    def process_data(data):
        print(SeverityScore.default_param1)
        return data
