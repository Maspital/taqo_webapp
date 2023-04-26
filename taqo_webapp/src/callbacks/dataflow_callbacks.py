from dash import Output, Input, State, ALL, callback_context
import plotly.graph_objs as go

import ast

import src.data_processor as dp
import src.graph_creator as gc


def get_callbacks(app):
    @app.callback(
        Output("state_selected_datasets", "data"),
        Input({"type": "dataset_select_checkbox", "index": ALL}, "checked"),
    )
    def set_current_datasets(checkbox_state):
        # List items are conveniently ordered by the index of the checkboxes
        selected_dataset_indexes = []
        for index, state in enumerate(checkbox_state):
            if state:
                selected_dataset_indexes.append(index)
        return selected_dataset_indexes

    @app.callback(
        Output("state_selected_pipelines", "data"),
        Input({"type": "pipeline_select_dropdown", "index": ALL}, "value"),
    )
    def set_current_pipelines(list_of_pipes):
        new_pipelines = {}

        for category in list_of_pipes:
            if category:
                for pipe in category:
                    cat, func = pipe.split("§")
                    new_pipelines.setdefault(cat, [])
                    new_pipelines[cat].append(func)

        return new_pipelines

    @app.callback(
        Output('state_processed_data', 'data'),
        Input('state_selected_datasets', 'data'),
        Input('state_selected_pipelines', 'data')
    )
    def process_data(data, pipes):
        if data is not None and pipes:
            processed_data = dp.execute_pipelines(data, pipes)
            return processed_data
        else:
            return None

    @app.callback(
        Output("bar_chart", "figure"),
        Input("state_processed_data", "data")
    )
    def create_bar_chart(processed_data):
        if processed_data:
            return gc.create_bar_chart(processed_data)
        else:
            return go.Figure()

    @app.callback(
        Output("bar_chart2", "figure"),
        Input("state_processed_data", "data")
    )
    def create_second_bar_chart(processed_data):
        if processed_data:
            return gc.create_bar_chart(processed_data)
        else:
            return go.Figure()

    @app.callback(
        Output("bar_chart3", "figure"),
        Input("state_processed_data", "data")
    )
    def create_third_bar_chart(processed_data):
        if processed_data:
            return gc.create_bar_chart(processed_data)
        else:
            return go.Figure()
