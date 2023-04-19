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

    def process_data(self, data):
        print(self.default_param1)
        return data
