# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from os import path

from src.modules import dataset_cards, handler, pipeline_cards
from src.callbacks import dataflow_callbacks

app = Dash(__name__,
           # Select theme here https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           # prevent_initial_callbacks=True,
           assets_url_path="/assets/",
           )
datasets = handler.get_datasets()
pipelines = handler.get_pipelines("./pipelines/")

app.layout = html.Div(
    [
        dcc.Store(id="selected_dataset"),
        dcc.Store(id="selected_pipelines"),
        dcc.Store(id="processed_data"),
        dcc.Store(id="state_last_selected_dataset"),

        dbc.Stack(
            [
                html.Div([
                    html.Img(
                        src="assets/taqo.png",
                        style={
                            "paddingRight": "10px",
                            "maxWidth": "100px",
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
                                dbc.Col(dataset_cards.dataset_card(path, index, app), width=3)
                                for index, path
                                in enumerate(datasets)
                            ],
                            style={
                                "justifyContent": "left",
                            }
                        )
                    ],
                    title="Datasets",
                ),
                dbc.AccordionItem(
                    pipeline_cards.create_pipeline_view(pipelines),
                    title="RBA Pipelines",
                ),
                dbc.AccordionItem(
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id="bar_chart"), width=4,
                            ),
                            dbc.Col(
                                dcc.Graph(id="bar_chart2"), width=4,
                            ),
                            dbc.Col(
                                dcc.Graph(id="bar_chart3"), width=4,
                            )
                        ]
                    ),
                    title="Evaluation",
                    style={
                        "display": "block"
                    }
                ),
            ],
            start_collapsed=False,
            always_open=True,
        ),
    ]
)

dataflow_callbacks.get_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
