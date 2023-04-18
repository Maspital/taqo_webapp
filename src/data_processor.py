import importlib
import json

from src.modules.handler import get_datasets


def execute_pipelines(dataset_index, pipelines):
    pipelines = retrieve_pipeline_functions(pipelines)
    dataset = retrieve_dataset(dataset_index)

    dataset = prepare_data(dataset)
    final_datasets = {}

    for category, pipes in pipelines.items():
        temp_data = dataset

        for pipe in pipes:
            temp_data = pipe(temp_data)

        temp_data = finalize_data(temp_data)
        final_datasets[category] = temp_data

    return final_datasets


def retrieve_pipeline_functions(pipelines):
    # Currently we only have string representations of the functions, we need to fetch the
    # actual functions from the corresponding module (= category)
    pipeline_dir = "pipelines"
    function_dict = {}

    for category, function_list in pipelines.items():
        module_name = category.lower().replace(" ", "_").replace("-", "_")
        module = importlib.import_module(f"{pipeline_dir}.{module_name}", module_name)

        funcs_to_add = []
        for func in function_list:
            class_name, function_name = func.split(".")
            class_ref = getattr(module, class_name)

            function_object = getattr(class_ref, function_name)
            funcs_to_add.append(function_object)

        function_dict[category] = funcs_to_add

    return function_dict


def retrieve_dataset(dataset_index):
    dateset = get_datasets()[dataset_index]
    with open(dateset) as file:
        lines = file.readlines()
        json_objects = [json.loads(line) for line in lines]

    return json_objects


def prepare_data(dataset):
    return dataset


def finalize_data(dataset):
    return dataset
