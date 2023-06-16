from dash import Output, Input

import src.data_processor as dp


def get_callbacks(app):
    @app.callback(
        Output("state_processed_data", "data"),
        Input("state_pipelines", "data"),
        Input("state_selected_datasets", "data"),

    )
    def process_data(pipelines, dataset_indexes):
        if not pipelines or not dataset_indexes:
            return None
        return dp.execute_pipelines(pipelines, dataset_indexes)
