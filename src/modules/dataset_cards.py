from dash import html
import dash_bootstrap_components as dbc
from dash import Output, Input


def dataset_card(title, index, app):
    base_color = "#FFFFFF"
    pressed_color = "#09b2ac"

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
                               n_clicks=0,
                               ),
                ],
            ),
        ],
        id={
            "type": "dataset_card",
            "index": index
        },
        color=base_color,
    )

    @app.callback(
        Output({"type": "dataset_card", "index": index}, "color"),
        Input("selected_dataset", "data"),
    )
    def update_card_style(last_button):
        # If this card contains the last pressed button, set the color to the pressed color
        if index == last_button:
            return pressed_color
        # Otherwise, set the color to the base color
        else:
            return base_color

    return card
