CATEGORY = "Trivial Uncorrelated"


class SeverityScore:
    title = "Severity Score"
    description = """
    Assign a risk score according to the SRE severity value.
    """

    required_fields = [
        "event.severity",
    ]

    @staticmethod
    def process_data(data):
        return data
