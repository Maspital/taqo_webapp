import os
from dash import Dash, dcc, html, Input, Output


def get_datasets():
    dataset_dir = "./datasets/"

    datasets = []
    for path in os.listdir(dataset_dir):
        if os.path.isfile(os.path.join(dataset_dir, path)):
            datasets.append(dataset_dir + path)

    return datasets

