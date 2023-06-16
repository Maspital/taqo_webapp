from dash import html, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


def dataset_card(dataset: dict, button_index: int, app):
    base_color = "#FFFFFF"
    pressed_color = "#09b2ac"

    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(dataset["name"], className="card-title"),
                    html.P(
                        dataset["description"],
                        className="card-text",
                    ),
                    dmc.Checkbox(
                        id={
                            "type": "dataset_select_checkbox",
                            "index": button_index,
                        },
                        label="Use dataset?"
                    )
                ],
            ),
        ],
        id={
            "type": "dataset_card",
            "index": button_index
        },
        color=base_color,
    )

    # Register a separate callback for each created button
    @app.callback(
        Output({"type": "dataset_card", "index": button_index}, "color"),
        Input("state_selected_datasets", "data"),
    )
    def update_card_style(toggled_buttons):
        if toggled_buttons and button_index in toggled_buttons:
            return pressed_color
        else:
            return base_color

    return card
