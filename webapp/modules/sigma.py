from src.module_src import sigma_score


class CapecScore:
    title = "Sigma Score"
    id = "260dbe1d7613bc832c59ca6c8d4bfb8c"
    description = """
    Assigns a risk score based on the sigma "level" field, if it exists.
    """

    required_fields = [
        "rule.level",
    ]

    @staticmethod
    def process_data(data):
        data = sigma_score.process(data)
        return data
