import json
from pathlib import Path
from copy import deepcopy

from src.backend.handler import get_datasets, get_modules_as_dict
from src.backend.utils import get_webapp_root
from src.backend.data_post_processor import finalize_data, finalize_metadata


def execute_pipelines(pipelines, dataset_indexes):
    pipelines = retrieve_pipeline_functions(pipelines)
    datasets, dataset_names = retrieve_datasets(dataset_indexes)

    prepped_data = prepare_data(datasets)
    final_datasets = {}

    for pipe_id, module in pipelines.items():
        temp_data = deepcopy(prepped_data)

        for module_func in module:
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
        filename = Path(all_datasets[index]["filename"])
        full_path = get_webapp_root() / ".." / "datasets" / filename

        with open(full_path, "r", encoding="utf-8") as file:
            for line in file:
                combined_data.append(json.loads(line))

    return combined_data, dataset_names


def prepare_data(dataset: list[dict]):
    fp_count = 0
    tp_count = 0
    for index, alert in enumerate(dataset):
        if alert["metadata"]["misuse"]:
            tp_count += 1
        else:
            fp_count += 1
        # ensure certain fields are always present no matter the active modules
        alert.setdefault("event", {})
        alert["event"].setdefault("event", {})
        dataset[index] = alert

    prep_data = {
        "data": dataset,
        "fp_count": fp_count,
        "tp_count": tp_count,
    }
    return prep_data
