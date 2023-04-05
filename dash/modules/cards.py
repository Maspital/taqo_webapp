from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def dataset_card(title, active_set, index):
    button_disabled = False
    style = {}
    if title == active_set:
        button_disabled = True
        style = {
            "backgroundColor": "#ceedeb"
        }

    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(title.split("/")[-1], className="card-title"),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button("Activate dataset",
                               color="primary",
                               disabled=button_disabled,
                               id={
                                   "type": "dataset_select",
                                   "index": index,
                               },
                               ),
                ]
            ),
        ],
        style=style
    )

    return card


def pipeline_card():
    pass


def graph_card():
    pass
