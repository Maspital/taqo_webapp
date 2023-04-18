from dash import html
import dash_bootstrap_components as dbc


def dataset_card(title, index):
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(title.split("/")[-1], className="card-title"),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button("Activate dataset",
                               color="primary",
                               id={
                                   "type": "dataset_select_button",
                                   "index": index,
                               },
                               ),
                ]
            ),
        ],
    )

    return card
