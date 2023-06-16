# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from src.modules import dataset_cards, handler, pipelines, graphs, module_preview, misc
from src.callbacks import (
    pipeline_callbacks,
    content_callbacks,
    parameter_callbacks,
    processing_callbacks,
    graph_callbacks,
)

app = Dash(
    __name__,
    # Select theme here https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
    ],
    assets_url_path="/assets/",
    prevent_initial_callbacks="initial_duplicate",
)

datasets = handler.get_datasets()
modules = handler.get_modules()

app.layout = html.Div(
    [
        dcc.Store(id="state_selected_datasets"),
        dcc.Store(id="state_pipelines", data={}),

        dcc.Store(id="state_graphs_to_render", data={}),
        dcc.Store(id="state_old_graphs_to_render", data={}),

        dcc.Store(id="state_processed_data", data={}),
        dcc.Store(
            id="state_last_action",
            data={
                # these keys must exist when changing this state, even if they are set to None
                "action": "",
                "pipe_id": "",
                "index": None,
                "module_id": None,
                "instance_id": None,
            },
        ),
        dcc.Store(id="state_module_ids", data=handler.get_module_ids()),
        # used to prevent incorrect callbacks by comparing old/new n_click values
        dcc.Store(id="state_mv_left_n_clicks", data=[]),
        dcc.Store(id="state_mv_right_n_clicks", data=[]),
        dbc.Stack(
            [
                html.Div(
                    [
                        html.Img(
                            src="assets/taqo.png",
                            style={
                                "paddingRight": "10px",
                                "maxWidth": "100px",
                            },
                        ),
                        html.Div(
                            [
                                html.H4("TAQOS"),
                                html.Div("Tactical Alert Quality Optimization System"),
                            ],
                            style={
                                "textAlign": "left",
                            },
                        ),
                    ],
                    style={"display": "flex"},
                ),
                html.Img(
                    src="assets/fkie.png",
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
                                dbc.Col(
                                    dataset_cards.dataset_card(path, index, app),
                                    width=3,
                                )
                                for index, path in enumerate(datasets)
                            ],
                            style={
                                "justifyContent": "left",
                            },
                        )
                    ],
                    title="Datasets",
                ),
                dbc.AccordionItem(
                    [
                        module_preview.create_module_preview(modules),
                        misc.large_visual_divider(),
                        pipelines.create_pipeline_view(),
                    ],
                    title="RBA Pipelines",
                ),
                dbc.AccordionItem(
                    [
                        graphs.create_graph_view(),
                    ],
                    title="Evaluation",
                    style={"display": "block"},
                ),
            ],
            start_collapsed=False,
            always_open=True,
        ),
    ]
)

pipeline_callbacks.get_callbacks(app)
content_callbacks.get_callbacks(app)
parameter_callbacks.get_callbacks(app)
processing_callbacks.get_callbacks(app)
graph_callbacks.get_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)


def run():
    app.run_server(debug=True)
