from dash import html, dcc
import dash_bootstrap_components as dbc


def create_pipeline_view(pipelines):
    """
    :param pipelines: Dict with category string as key and list of respective pipeline classes as values
    :return: Div element containing pipeline info and UI
    """
    number_of_categories = len(pipelines)
    view = []

    for index, (category, category_pipelines) in enumerate(pipelines.items()):
        view.append(pipeline_category(category, category_pipelines, index))
        if index < number_of_categories - 1:
            # Visual divider between categories
            view.append(html.Hr(style={
                "height": "10px",
                "color": "#333333"
            }))

    return html.Div(view)


def pipeline_category(category, list_of_pipes, index):
    result = html.Div([
        html.H5([category]),
        dcc.Dropdown(
            dropdown_list(list_of_pipes, category),
            multi=True,
            id={
                "type": "pipeline_select_dropdown",
                "index": f"{category}§{index}",
            },
            style={"paddingBottom": "3px"},
        ),
        dbc.Row(
            [
                dbc.Col(pipeline_card(pipeline), width=3)
                for pipeline
                in list_of_pipes
            ],
            style={"height": "100%"}),
    ])

    return result


def dropdown_list(list_of_pipes, category):
    result = []

    for pipe in list_of_pipes:
        result.append(
            # The value will look like this: "<CATEGORY>$<CLASS_NAME>.<FUNCTION_NAME>
            {"label": pipe.title, "value": f"{category}§{str(pipe.process_data).split()[1]}"}
        )
    return result


def pipeline_card(pipeline):
    required_fields = [
        html.Li(html.Code(field), style={"fontFamily": "monospace"})
        for field in pipeline.required_fields
    ]

    card = dbc.Card(
        dbc.CardBody(
            [
                html.H6(pipeline.title),
                html.P(
                    pipeline.description,
                    className="card-text",
                ),
                html.P(
                    ["Required fields:",
                     html.Ul(required_fields)
                     ],
                    className="card-text",
                ),
            ],
        )
    )

    return card
