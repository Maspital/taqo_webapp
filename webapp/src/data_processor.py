import json
import os.path
import itertools

from src.modules.handler import get_datasets, get_modules_as_dict
from src.utils import get_webapp_root


def execute_pipelines(pipelines, dataset_indexes):
    pipelines = retrieve_pipeline_functions(pipelines)
    datasets, dataset_names = retrieve_datasets(dataset_indexes)

    prepped_data = prepare_data(datasets)
    final_datasets = {}

    for pipe_id, modules_funcs in pipelines.items():
        temp_data = prepped_data.copy()

        for module_func in modules_funcs:
            func = module_func["processor_func"]
            params = module_func["parameters"]
            if params:
                temp_data = func(temp_data, params)
            else:
                temp_data = func(temp_data)

        temp_data = finalize_data(temp_data)
        final_datasets[pipe_id] = temp_data

    final_datasets = finalize_metadata(final_datasets, dataset_names)
    return final_datasets


def retrieve_pipeline_functions(pipelines):
    # returns a dict, with each key representing one pipeline and containing
    # module functions in the order they should be executed in
    function_dict = {}
    all_modules = get_modules_as_dict()

    for pipe_id, pipe_content in pipelines.items():
        function_dict[pipe_id] = []
        for module in pipe_content:
            step = {}
            instance = all_modules[module["module_id"]]
            step["processor_func"] = instance.process_data
            step["parameters"] = module["parameters"]
            function_dict[pipe_id].append(step)

    return function_dict


def retrieve_datasets(dataset_indexes: list[int]):
    all_datasets = get_datasets()
    combined_data = []
    dataset_names = []

    for index in dataset_indexes:
        dataset_names.append(all_datasets[index]["name"])
        path = all_datasets[index]["filename"]
        full_path = os.path.join(get_webapp_root(), "../datasets/", path)

        with open(full_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            combined_data.extend([json.loads(line) for line in lines])

    return combined_data, dataset_names


def prepare_data(dataset):
    fp_count = 0
    tp_count = 0
    for alert in dataset:
        if alert["metadata"]["misuse"]:
            tp_count += 1
        else:
            fp_count += 1
    prep_data = {
        "data": dataset,
        "fp_count": fp_count,
        "tp_count": tp_count,
    }
    return prep_data


def finalize_data(dataset: dict):
    severities = get_unique_severities(dataset["data"])

    num_tps_weighted = [0] * len(severities)
    num_sres_weighted = [0] * len(severities)
    num_techs_weighted = [0] * len(severities)

    viewed_techs_per_severity = {}
    for sev in severities:
        viewed_techs_per_severity.setdefault(sev, [])

    for sre in dataset["data"]:
        risk_score = sre["event"]["event"]["risk_score"]
        risk_score_index = severities.index(risk_score)

        techniques = get_techniques(sre["metadata"].get("mitreattack"))
        viewed_techs_per_severity[risk_score].extend(techniques)

        num_sres_weighted[risk_score_index] += 1
        if sre["metadata"]["misuse"]:
            num_tps_weighted[risk_score_index] += 1

    num_techs_weighted = count_techs_per_severity(
        viewed_techs_per_severity, num_techs_weighted, severities)

    for i in range(1, len(severities)):
        num_sres_weighted[i] += num_sres_weighted[i - 1]
        num_tps_weighted[i] += num_tps_weighted[i - 1]
        num_techs_weighted[i] += num_techs_weighted[i - 1]

    dataset["num_sres_weighted"] = num_sres_weighted
    dataset["num_sres_weighted_extended"] = [0] + num_sres_weighted
    dataset["num_tps_weighted"] = num_tps_weighted
    dataset["num_tps_weighted_extended"] = [0] + num_tps_weighted
    dataset["num_techs_weighted"] = num_techs_weighted
    dataset["num_techs_weighted_extended"] = [0] + num_techs_weighted
    dataset["list_risk_scores"] = severities

    return dataset


def get_techniques(mitreattack_field: dict[list]) -> list[str]:
    if mitreattack_field:
        techniques = list(mitreattack_field.values())
        return list(itertools.chain.from_iterable(techniques))
    else:
        return []


def get_unique_severities(data: list[dict]) -> list:
    return sorted(set(sre["event"]["event"]["risk_score"] for sre in data))


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
