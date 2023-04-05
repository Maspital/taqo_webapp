# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash import Input, Output, State, MATCH, ALL

import ast

from modules import cards, handler

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           prevent_initial_callbacks=True,
           )
datasets = handler.get_datasets()

app.layout = html.Div(
    [
        dcc.Store(id="global_store"),

        dbc.Stack(
            [
                html.Div([
                    html.Img(
                        src="assets/taqo.png",
                        style={
                            "paddingRight": "10px",
                        }
                    ),
                    html.Div([
                        html.H4("TAQOS"),
                        html.Div("Tactical Alert Quality Optimization System")
                    ],
                        style={
                            "textAlign": "left",
                        }
                    ),
                ], style={"display": "flex"}),
                html.Img(src="assets/fkie.png",
                         style={"height": "12%", "width": "12%", "maxWidth": "200px"},
                         ),
            ],
            direction="horizontal",
            style={
                "backgroundImage": "linear-gradient(to right, #015375, #09b2ac)",
                "color": "#FFFFFF",
                "padding": "10px",
                "display": "flex",
                "justifyContent": "space-between",
            },
        ),

        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(cards.dataset_card(path, "Something", index)) for index, path in
                                enumerate(datasets)
                            ],
                            style={
                                "justifyContent": "left",
                            }
                        )
                    ],
                    title="Datasets",
                ),
                dbc.AccordionItem(
                    [
                        html.P("This is the content of the second section"),
                        dbc.Button("Don't click me!", color="danger"),
                    ],
                    title="RBA Pipelines",
                ),
                dbc.AccordionItem(
                    title="Evaluation",
                    id="eval_output",
                ),
            ],
            start_collapsed=False,
            always_open=True,
        ),
    ]
)


@app.callback(
    Output("eval_output", "children"),
    Input({"type": "dataset_select", "index": ALL}, "n_clicks"),
    State({"type": "dataset_select", "index": ALL}, "children"),
    prevent_initial_call=True,
)
def current_dataset(*args):
    print(args)
    # The callback context contains the original id we assigned to the button that triggered the current callback
    # This id corresponds to the dataset we want to access. Need to use ast because its a string repr. of a dict
    pressed_button = ast.literal_eval(callback_context.triggered[0]["prop_id"].split(".")[0])
    dataset_index = pressed_button["index"]
    if dataset_index is not None:
        return f"Pressed button: {datasets[dataset_index]}"
    return "No button pressed."


# next, use https://dash.plotly.com/dash-core-components/store to manage handling of chosen dataset


if __name__ == '__main__':
    app.run_server(debug=True)
