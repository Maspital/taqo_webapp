from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify as Icon

from uuid import uuid4

from src.backend import handler
from src.layout import module_cards


def create_pipeline_view():
    view = [
        title_and_ui(),
        html.Div(id="pipeline_layout"),
    ]

    return html.Div(view)


def title_and_ui():
    result = dbc.Row(
        [
            dbc.Col(html.H5("Pipelines"), width=1),
            dbc.Col(dbc.Button(
                Icon(icon="bi:plus", style={"fontSize": "150%"}),
                className="me-1",
                id="add_pipeline_button",
            ),
                width=1,
            ),
        ],
        justify="between"
    )

    return result


def add_pipeline(current_pipes, new_pipe_name):
    if not current_pipes:
        current_pipes = [html.Hr()]
    else:
        current_pipes.append(html.Hr())

    new_pipe_id = str(uuid4()) + f".Pipe {new_pipe_name}"

    new_pipe = [
        dbc.Row(
            [
                dbc.Col(html.H6(f"Pipe {new_pipe_name}"), width=1),
                dbc.Col(
                    dbc.Button(
                        Icon(icon="bi:trash"),
                        color="danger",
                        className="me-1",
                        id={
                            "type": "pipeline_delete_button",
                            "pipe_id_to_delete": new_pipe_id,
                        },
                    ),
                    width=1,
                ),
            ],
            justify="between",
        ),
        html.P(),
        dbc.Row(
            dbc.Col("Add modules to this pipeline..."),
            id={"type": "pipeline_module_row", "id": new_pipe_id},
            justify="start",
            style={
                "overflowX": "auto",    # browser will handle horizontal overflow and provide a scroll bar
                "display": "flex",      # allows control the layout of its child elements
                "flexWrap": "nowrap",   # prevents the flex container from wrapping its children onto multiple lines
            },
        )
    ]
    current_pipes.append(html.Div(
        new_pipe,
        id={
            "type": "single_pipeline",
            "name": f"Pipe {new_pipe_name}",
            "id": new_pipe_id,
        },
    ))
    return current_pipes


def remove_pipeline(current_pipes, id_to_remove):
    # find the Div container corresponding to the pipeline
    index = next((i for i, item in enumerate(current_pipes)
                  if item.get('props', {}).get('id', {}).get('id') == id_to_remove), -1)
    # remove the pipe itself as well as the Hr element above it
    current_pipes.pop(index - 1)
    current_pipes.pop(index - 1)

    return current_pipes


def modify_layout(current_layout, action, layout_index):
    # somewhat convoluted, but this way visuals and data are fully separated
    # the index affected corresponds to the index of a dbc card within the row layout
    action_taken = action["action"]
    pipe_id = action["pipe_id"]
    instance_id = action["instance_id"]
    index = action["index"]     # single integer for "delete, list with two integers for "swap"
    module_id = action["module_id"]

    if action_taken == "add":
        all_modules = handler.get_modules_as_dict()
        new_module_object = dbc.Col(
            module_cards.create_module_card(all_modules[module_id], pipe_id, instance_id),
            width="auto",
            style={
                "flexShrink": "0",  # prevents the column from shrinking if there's not enough room in the row
                "width": "25%"      # fixed width for each column/module card
            },
        )
        if type(current_layout[layout_index]) is not list:
            # initialize row content as list
            # this will only be the case if there were no modules before
            current_layout[layout_index] = []
        current_layout[layout_index].append(new_module_object)

    elif action_taken == "delete":
        del current_layout[layout_index][index]

    elif action_taken == "delete_pipe_empty":
        current_layout[layout_index] = dbc.Col("Add modules to this pipeline...")

    elif action_taken == "swap":
        current_layout[layout_index][index[0]], current_layout[layout_index][index[1]] = \
            current_layout[layout_index][index[1]], current_layout[layout_index][index[0]]

    return current_layout
