from dash import Output, Input

import src.backend.data_processor as dp


def get_callbacks(app):
    @app.callback(
        Output("state_processed_data", "data"),
        Input("state_pipelines", "data"),
        Input("state_selected_datasets", "data"),
    )
    def callback_process_data(pipelines, dataset_indexes):
        return process_data(pipelines, dataset_indexes)


def process_data(pipelines, dataset_indexes):
    if not pipelines or not dataset_indexes:
        return None
    return dp.execute_pipelines(pipelines, dataset_indexes)
