from dash import Output, Input, State, ALL, ctx
from dash.exceptions import PreventUpdate

from uuid import uuid4


def get_callbacks(app):
    @app.callback(
        Output("state_graphs_to_render", "data"),
        Input("create_graph_button", "n_clicks"),
        State("state_graphs_to_render", "data"),
        State("graph_x_selection_radio", "value"),
        State("graph_y_selection_radio", "value"),
    )
    def callback_add_graph_to_state(n_clicks, graphs_state, x_axis, y_axis):
        return add_graph_to_state(n_clicks, graphs_state, x_axis, y_axis)

    @app.callback(
        Output("state_graphs_to_render", "data", allow_duplicate=True),
        Input({
            "type": "delete_graph_button", "graph_to_delete": ALL,
        }, "n_clicks"),
        State("state_graphs_to_render", "data"),
    )
    def callback_remove_graph_from_state(del_button_press_count, graph_state):
        return remove_graph_from_state(del_button_press_count, graph_state)


def add_graph_to_state(n_clicks, graphs_state, x_axis, y_axis):
    if not n_clicks:
        raise PreventUpdate
    new_graph_id = str(uuid4())
    graphs_state[new_graph_id] = {
        "x_axis": x_axis,
        "y_axis": y_axis,
        "options": {},
    }
    return graphs_state


def remove_graph_from_state(del_button_press_count, graph_state):
    if any(item is not None for item in del_button_press_count):
        del graph_state[ctx.triggered_id["graph_to_delete"]]
        return graph_state
    else:
        raise PreventUpdate
