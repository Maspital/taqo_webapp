def finalize_data(dataset: dict):
    severities = get_unique_severities(dataset["data"])

    num_tps_weighted = [0] * len(severities)
    num_fps_weighted = [0] * len(severities)
    num_sres_weighted = [0] * len(severities)
    num_techs_weighted = [0] * len(severities)

    viewed_techs_per_severity = {}
    for sev in severities:
        viewed_techs_per_severity.setdefault(sev, [])

    for sre in dataset["data"]:
        # if the risk score has never been set by any module, just take 0
        risk_score = sre["event"]["event"].get("risk_score", 0)
        risk_score_index = severities.index(risk_score)

        techniques = get_techniques(sre["metadata"].get("mitreattack"))
        viewed_techs_per_severity[risk_score].extend(techniques)

        num_sres_weighted[risk_score_index] += 1
        if sre["metadata"]["misuse"]:
            num_tps_weighted[len(severities) - 1 - risk_score_index] += 1
        else:
            num_fps_weighted[len(severities) - 1 - risk_score_index] += 1

    num_techs_weighted = count_techs_per_severity(
        viewed_techs_per_severity, num_techs_weighted, severities)

    num_sres_weighted = num_sres_weighted[::-1]

    for i in range(1, len(severities)):
        num_sres_weighted[i] += num_sres_weighted[i - 1]
        num_tps_weighted[i] += num_tps_weighted[i - 1]
        num_fps_weighted[i] += num_fps_weighted[i - 1]
        num_techs_weighted[i] += num_techs_weighted[i - 1]

    dataset["num_sres_weighted"] = num_sres_weighted
    dataset["num_sres_weighted_extended"] = [0] + num_sres_weighted
    dataset["num_tps_weighted"] = num_tps_weighted
    dataset["num_tps_weighted_extended"] = [0] + num_tps_weighted
    dataset["num_fps_weighted"] = num_fps_weighted
    dataset["num_fps_weighted_extended"] = [0] + num_fps_weighted
    dataset["num_techs_weighted"] = num_techs_weighted
    dataset["num_techs_weighted_extended"] = [0] + num_techs_weighted
    dataset["list_risk_scores"] = severities
    return dataset


def get_techniques(mitreattack_field: dict[list]) -> list[str]:
    if mitreattack_field:
        return [technique for techniques in mitreattack_field.values() for technique in techniques]
    else:
        return []


def get_unique_severities(data: list[dict]) -> list:
    # if the risk score has never been set by any module, just take 0
    return sorted(set(sre["event"]["event"].get("risk_score", 0) for sre in data))


def count_techs_per_severity(
        viewed_techs: dict, num_techs_weighted: list[int], severities: list[int]) -> list[int]:
    # only count new techniques that were not seen in any previous (lower) risk score
    previous_techs = set()
    for risk_score, current_techs in viewed_techs.items():
        current_unique_techs = set(current_techs)
        total_techs = previous_techs | current_unique_techs
        num_of_new_techs = len(total_techs) - len(previous_techs)
        num_techs_weighted[severities.index(risk_score)] = num_of_new_techs
        previous_techs = total_techs

    return num_techs_weighted


def finalize_metadata(final_dataset: dict, dataset_names: list[str]) -> dict:
    for pipe_id in final_dataset.keys():
        final_dataset[pipe_id].setdefault("metadata", {})
        final_dataset[pipe_id]["metadata"]["used_source"] = dataset_names
    return final_dataset
