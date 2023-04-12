from dash import Output, Input, State, ALL, callback_context

import ast


def get_callbacks(app):
    @app.callback(
        Output("selected_dataset", "data"),
        Input({"type": "dataset_select_button", "index": ALL}, "n_clicks"),
        State({"type": "dataset_select_button", "index": ALL}, "children"),
        prevent_initial_call=True,
    )
    def set_current_dataset(*args):
        # The callback context contains the original id we assigned to the button that triggered the current callback
        # This id corresponds to the dataset we want to access
        #
        # Need to use ast because it's a string representation of a dict
        pressed_button = ast.literal_eval(callback_context.triggered[0]["prop_id"].split(".")[0])
        dataset_index = pressed_button["index"]
        return dataset_index

    @app.callback(
        Output("selected_pipelines", "data"),
        Input({"type": "pipeline_select_dropdown", "index": ALL}, "value"),
    )
    def set_current_pipelines(list_of_pipes):
        new_pipelines = {}
        for pipes in list_of_pipes:
            if pipes:
                for pipe in pipes:
                    pipe = ast.literal_eval(pipe)
                    category = pipe["category"]
                    new_pipelines.setdefault(category, [])
                    new_pipelines[category].append(pipe)

        return str(new_pipelines)

    # @app.callback(
    #     Output("selected_pipelines", "data"),
    #     Input("pipeline_select_dropdown", "value")
    # )
    # def set_pipelines(value):
    #     return value

    @app.callback(
        Output('graph', 'children'),
        Input('selected_dataset', 'data'),
        Input('selected_pipelines', 'data')
    )
    def create_graph(data, pipes):
        return f"{data} + {pipes}"
