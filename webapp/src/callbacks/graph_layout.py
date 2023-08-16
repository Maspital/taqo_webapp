from dash import Output, Input, State
from dash.exceptions import PreventUpdate

from src.layout.graphs import add_graph, delete_graph


def get_callbacks(app):
    @app.callback(
        Output("graph_creation_modal", "is_open"),
        Input("add_graph_button", "n_clicks"),
        Input("create_graph_button", "n_clicks"),
        State("graph_creation_modal", "is_open"),
    )
    def callback_toggle_modal(n1, n2, is_open):
        return toggle_modal(n1, n2, is_open)

    @app.callback(
        Output("graph_layout", "children"),
        Output("state_old_graphs_to_render", "data"),
        Input("state_graphs_to_render", "data"),
        State("state_old_graphs_to_render", "data"),
        State("state_processed_data", "data"),
        State("graph_layout", "children"),
        prevent_initial_update=True,
    )
    def callback_add_or_remove_graph(graph_state, old_graphs, data, layout):
        return add_or_remove_graph(graph_state, old_graphs, data, layout)

    @app.callback(
        Output("graph_layout", "children", allow_duplicate=True),
        Input("state_processed_data", "data"),
        State("state_graphs_to_render", "data"),
    )
    def callback_update_charts(processed_data, graphs_to_render):
        return update_charts(processed_data, graphs_to_render)


def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def add_or_remove_graph(graph_state, old_graphs, data, layout):
    if not layout:
        layout = []
    if not graph_state:
        graph_state = {}
    new = set(graph_state) if graph_state else set()
    old = set(old_graphs)
    if new > old:
        # graph has been added
        new_graph_id = list(new - old)[0]
        new_graph = graph_state[new_graph_id]
        layout = add_graph(layout, new_graph, new_graph_id, data)
    elif old > new:
        # graph has been deleted
        id_to_delete = list(old - new)[0]
        layout = delete_graph(layout, id_to_delete, old_graphs)
    else:
        raise PreventUpdate
    return layout, graph_state


def update_charts(processed_data, graphs_to_render):
    if graphs_to_render:
        new_layout = []
        for graph_id, graph in graphs_to_render.items():
            new_layout = add_graph(new_layout, graph, graph_id, processed_data)
        return new_layout
    else:
        raise PreventUpdate
