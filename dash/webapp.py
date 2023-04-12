# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from modules import dataset_cards, handler, pipeline_cards
from callbacks import get_callbacks

app = Dash(__name__,
           # Select theme here https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           prevent_initial_callbacks=True,
           )
datasets = handler.get_datasets()
pipelines = handler.get_pipelines("./pipelines/")

app.layout = html.Div(
    [
        dcc.Store(id="selected_dataset"),
        dcc.Store(id="selected_pipelines"),
        dcc.Store(id="created_graphs"),

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
                                dbc.Col(dataset_cards.dataset_card(path, index), width=3)
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
                    title="Evaluation",
                    id="graph",
                ),
            ],
            start_collapsed=False,
            always_open=True,
        ),
    ]
)


get_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
