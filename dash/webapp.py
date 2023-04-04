# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        # dbc.Row(
        #     [
        #         dbc.Col(html.Img(src="assets/taqo.png", style={"height": "20%", "width": "20%"})),
        #         dbc.Col([
        #             html.Div([
        #                 html.H3("TAQOS"),
        #                 html.Span("Tactical Alert Quality Optimization System")
        #             ],
        #                 style={"textAlign": "left"})
        #         ]),
        #         dbc.Col(html.Img(src="assets/fkie.png",
        #                          style={"height": "40%", "width": "40%", }),
        #                 style={"height": "60%"}
        #                 ),
        #     ],
        #     justify="between",
        #     align="center",
        #     style={
        #         "backgroundImage": "linear-gradient(to right, #015375, #09b2ac)",
        #         "color": "#FFFFFF",
        #         "padding": "20px",
        #     }
        # ),
        dbc.Stack([
            html.Img(src="assets/taqo.png", style={"margin-right": "20px"}),
            html.Div([
                html.H4("TAQOS"),
                html.Div("Tactical Alert Quality Optimization System")
            ],
                style={
                    "textAlign": "left",
                }
            ),
            html.Img(src="assets/fkie.png",
                     style={"height": "12%", "width": "12%"},
                     ),
        ],
            direction="horizontal",
            style={
                "backgroundImage": "linear-gradient(to right, #015375, #09b2ac)",
                "color": "#FFFFFF",
                "padding": "10px",
                "justifyContent": "space-between"
            },
        ),

        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P("This is the content of the first section"),
                        dbc.Button("Click here"),
                    ],
                    title="Item 1",
                ),
                dbc.AccordionItem(
                    [
                        html.P("This is the content of the second section"),
                        dbc.Button("Don't click me!", color="danger"),
                    ],
                    title="Item 2",
                ),
                dbc.AccordionItem(
                    "This is the content of the third section",
                    title="Item 3",
                ),
            ],
            start_collapsed=False,
            always_open=True,
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
