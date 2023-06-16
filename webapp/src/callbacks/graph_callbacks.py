from dash import Output, Input, State, ALL, ctx
from dash.exceptions import PreventUpdate

from uuid import uuid4

from src.modules.graphs import add_graph, delete_graph


def get_callbacks(app):
    @app.callback(
        Output("graph_creation_modal", "is_open"),
        [
            Input("add_graph_button", "n_clicks"),
            Input("create_graph_button", "n_clicks")
        ],
        [
            State("graph_creation_modal", "is_open"),
        ],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        Output("state_graphs_to_render", "data"),
        [
            Input("create_graph_button", "n_clicks"),
        ],
        [
            State("state_graphs_to_render", "data"),
            State("graph_x_selection_radio", "value"),
            State("graph_y_selection_radio", "value"),
        ],
    )
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

    @app.callback(
        Output("state_graphs_to_render", "data", allow_duplicate=True),
        [
            Input({
                "type": "delete_graph_button", "graph_to_delete": ALL,
            }, "n_clicks"),
        ],
        [
            State("state_graphs_to_render", "data"),
        ],
    )
    def remove_graph_from_state(del_button_press_count, graph_state):
        if any(item is not None for item in del_button_press_count):
            del graph_state[ctx.triggered_id["graph_to_delete"]]
            return graph_state
        else:
            raise PreventUpdate

    @app.callback(
        Output("graph_layout", "children"),
        Output("state_old_graphs_to_render", "data"),
        [
            Input("state_graphs_to_render", "data"),
        ],
        [
            State("state_old_graphs_to_render", "data"),
            State("state_processed_data", "data"),
            State("graph_layout", "children"),
        ],
        prevent_initial_update=True,
    )
    def add_or_remove_graph(graph_state, old_graphs, data, layout):
        if not layout:
            layout = []
        new = set(graph_state)
        old = set(old_graphs)
        if new > old:
            # graph has been added
            new_graph_id = list(new-old)[0]
            new_graph = graph_state[new_graph_id]
            layout = add_graph(layout, new_graph, new_graph_id, data)
        elif old > new:
            # graph has been deleted
            id_to_delete = list(old - new)[0]
            layout = delete_graph(layout, id_to_delete, old_graphs)
        else:
            raise PreventUpdate

        return layout, graph_state

    @app.callback(
        Output("graph_layout", "children", allow_duplicate=True),
        [
            Input("state_processed_data", "data"),
        ],
        [
            State("state_graphs_to_render", "data")
        ],
    )
    def update_charts(processed_data, graphs_to_render):
        if graphs_to_render:
            new_layout = []
            for graph_id, graph in graphs_to_render.items():
                new_layout = add_graph(new_layout, graph, graph_id, processed_data)
            return new_layout
        else:
            raise PreventUpdate
