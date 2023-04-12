from dash import Dash, html, dcc, callback_context, Input, Output, State, ALL
import dash_bootstrap_components as dbc


def pipeline_category(category, list_of_pipes, cur, total):
    if cur < total:
        divider = html.Hr(style={
            "height": "10px",
            "color": "#333333"
        })
    else:
        divider = None

    category_norm = category.replace("-", "_").replace(" ", "_").lower()

    result = html.Div([
        html.H5([category]),
        dcc.Dropdown(
            dropdown_list(list_of_pipes),
            multi=True,
            id={
                "type": "pipeline_select_dropdown",
                "index": f"{cur}",
                },
            style={"paddingBottom": "2px"},
        ),
        dbc.Row(
            [
                dbc.Col(pipeline_card(pipeline), width=3)
                for pipeline
                in list_of_pipes
            ]),
        divider,
    ])

    return result


def dropdown_list(list_of_pipes):
    result = []

    for pipe in list_of_pipes:
        result.append(
            {"label": pipe["name"], "value": str(pipe)}
        )
    return result


def pipeline_card(pipeline):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H6(pipeline["name"]),
                html.P(
                    pipeline["description"],
                    className="card-text",
                ),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
            ],
        )
    )

    return card
