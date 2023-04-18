from dash import Output, Input, State, ALL, callback_context

import ast

import src.data_processor as dp


def get_callbacks(app):
    @app.callback(
        Output("selected_dataset", "data"),
        Input({"type": "dataset_select_button", "index": ALL}, "n_clicks"),
        State({"type": "dataset_select_button", "index": ALL}, "children"),
        prevent_initial_call=True,
    )
    def set_current_dataset(*args):
        pressed_button = ast.literal_eval(callback_context.triggered[0]["prop_id"].split(".")[0])
        dataset_index = pressed_button["index"]
        return dataset_index

    @app.callback(
        Output("selected_pipelines", "data"),
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
        Output('graph', 'children'),
        Input('selected_dataset', 'data'),
        Input('selected_pipelines', 'data')
    )
    def create_graph(data, pipes):
        if pipes:
            dp.execute_pipelines(data, pipes)
        return f"{data} + {pipes}"
