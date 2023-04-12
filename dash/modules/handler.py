import os
import yaml


def get_datasets():
    dataset_dir = "./datasets/"

    datasets = []
    for path in os.listdir(dataset_dir):
        if os.path.isfile(os.path.join(dataset_dir, path)):
            datasets.append(dataset_dir + path)

    return datasets


def get_pipelines():
    pipelines_dir = "./pipelines/"

    pipelines = []
    pipelines_grouped = {}
    for path in os.listdir(pipelines_dir):
        if os.path.isfile(os.path.join(pipelines_dir, path)):
            pipelines.append(pipelines_dir + path)

    for pipeline in pipelines:
        with open(pipeline) as file:
            yml = yaml.safe_load(file)
            category = yml["category"]
            pipelines_grouped.setdefault(category, [])
            pipelines_grouped[category].append(yml)

    return pipelines_grouped
