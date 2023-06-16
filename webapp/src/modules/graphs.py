from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify as Icon

from src.graph_creator import data_x, data_y, create_custom_chart


def create_graph_view():
    view = [
        title_and_ui(),
        html.Div(dbc.Row(
            [],
            id="graph_layout",
            justify="start",
        )),
        graph_creation_modal(),
    ]

    return html.Div(view)


def title_and_ui():
    result = dbc.Row(
        [
            dbc.Col(html.H5("Graphs"), width=1),
            dbc.Col(dbc.Button(
                Icon(icon="bi:plus", style={"fontSize": "150%"}),
                className="me-1",
                id="add_graph_button",
            ),
                width=1,
            ),
        ],
        justify="between"
    )
    return result


def graph_creation_modal():
    result = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Add evaluation graph")),
            dbc.ModalBody(graph_settings()),
            dbc.ModalFooter(
                dbc.Button(
                    "Create",
                    id="create_graph_button",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="graph_creation_modal",
        is_open=False,
    )
    return result


def graph_settings():
    options_x = [{"label": label, "value": value} for value, label in data_x().items()]
    options_y = [{"label": label, "value": value} for value, label in data_y().items()]
    result = [
        dmc.Text("Value mapped to x axis:"),
        dbc.RadioItems(
            options=options_x,
            value=options_x[0]["value"],
            id="graph_x_selection_radio",
        ),
        html.Br(),
        dmc.Text("Value mapped to y axis:"),
        dbc.RadioItems(
            options=options_y,
            value=options_y[0]["value"],
            id="graph_y_selection_radio",
        ),
    ]
    return result


def add_graph(layout: list, new_graph: dict, new_graph_id: str, data: dict) -> list:
    if not layout:
        layout = []
    layout.append(dbc.Col(
        [
            dbc.Card(
                [
                    dcc.Graph(
                        figure=create_custom_chart(new_graph, data),
                        id=new_graph_id,
                    ),
                    dbc.Button(
                        Icon(icon="bi:trash"),
                        color="light",
                        className="me-1",
                        id={
                            "type": "delete_graph_button",
                            "graph_to_delete": new_graph_id,
                        },
                    ),
                ]
            )
        ], width=4))
    return layout


def delete_graph(layout: list, graph_id: str, graph_state: dict) -> list:
    # position of the id within the state corresponds to the position in the layout
    index_to_delete = list(graph_state).index(graph_id)
    del layout[index_to_delete]
    return layout
