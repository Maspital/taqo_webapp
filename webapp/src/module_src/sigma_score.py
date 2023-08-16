def process(dataset):
    events = dataset["data"]

    for index, sre in enumerate(events):
        if "level" in sre["rule"]:
            sigma_score = get_sigma_score(sre)
            sre.setdefault("event", {})
            sre["event"].setdefault("event", {})
            sre["event"]["event"]["risk_score"] = sigma_score
            sre["event"]["event"]["base_score"] = sigma_score
        events[index] = sre

    dataset["data"] = events
    return dataset


def get_sigma_score(sre):
    score = get_numerical_score(sre["rule"]["level"])
    return score


def get_numerical_score(string_score):
    if not string_score:
        # Some entries don't have a certain score
        return None
    elif string_score == "informational":
        return 1
    elif string_score == "low":
        return 25
    elif string_score == "medium":
        return 50
    elif string_score == "high":
        return 75
    elif string_score == "critical":
        return 100
    else:
        raise ValueError("Unexpected score string")
