from dash import html
import dash_bootstrap_components as dbc

from more_itertools import batched


def create_module_preview(modules):
    view = []

    for module_group in batched(modules, 4):
        view.append(
            dbc.Row([
                dbc.Col(module_card(module), width=3)
                for module in module_group
            ],
                justify="start",
            )
        )

    view = add_visual_divider(view)
    view.insert(0, html.H5("Available Modules"))

    return html.Div(view)


def module_card(module):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H6(module.title),
                html.P(
                    module.description,
                    className="card-text",
                ),
                dbc.DropdownMenu(
                    label="Add to pipe",
                    children=[],
                    color="primary",
                    id={
                        "type": "pipeline_select_dropdown",
                        "id": module.id,
                    },
                    size="sm",
                )
            ],
        )
    )

    return card


def set_dropdown_options(pipeline_div, module_ids):
    pipes = []
    for item in pipeline_div:
        # obtain name and ID of all currently available pipelines
        if 'name' in item.get('props', {}).get('id', {}):
            pipe_name = item['props']['id']['name']
            pipe_id = item['props']['id']['id']
            pipes.append({'name': pipe_name, 'id': pipe_id})

    new_options = []
    for module_id in module_ids:
        single_module_options = []
        for pipe in pipes:
            single_module_options.append(
                dbc.DropdownMenuItem(
                    pipe["name"],
                    id={
                        "type": "pipeline_select_dropdown_button",
                        "pipe_id": pipe["id"],
                        "module_id": module_id,
                    }
                )
            )
        new_options.append(single_module_options)

    return new_options


def add_visual_divider(rows):
    result = []
    for row in rows:
        result.append(row)
        result.append(html.Hr())

    result.pop()
    return result
