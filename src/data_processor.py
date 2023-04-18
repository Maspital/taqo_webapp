import importlib
import json
import plotly.graph_objs as go

from src.modules.handler import get_datasets


def execute_pipelines(dataset_index, pipelines):
    pipelines = retrieve_pipeline_functions(pipelines)
    dataset = retrieve_dataset(dataset_index)

    prepped_data = prepare_data(dataset)
    final_datasets = {}

    for category, pipes in pipelines.items():
        temp_data = prepped_data.copy()

        for pipe in pipes:
            temp_data = pipe(temp_data)

        temp_data = finalize_data(temp_data)
        final_datasets[category] = temp_data

    return create_graph(final_datasets)


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
    fp_count = 0
    tp_count = 0
    for alert in dataset:
        if alert["metadata"]["misuse"]:
            tp_count += 1
        else:
            fp_count += 1
    prep_data = {
        "data": dataset,
        "total_fp_count": fp_count,
        "total_tp_count": tp_count,
                 }
    return prep_data


def finalize_data(dataset):
    return dataset


def create_graph(dataset):
    fig = go.Figure()

    for category, data in dataset.items():
        tp_count = data["total_tp_count"]
        fp_count = data["total_fp_count"]

        fig.add_trace(
            go.Bar(
                name=category,
                x=["TPs"],
                y=[tp_count],
                # offsetgroup=1,
            )
        )
        fig.add_trace(
            go.Bar(
                name=category,
                x=["FPs"],
                y=[fp_count],
                # offsetgroup=1,
            )
        )

    layout = go.Layout(
        title="Number of TPs and FPs for each category",
        barmode="group",
    )
    fig.update_layout(layout)
    return fig
