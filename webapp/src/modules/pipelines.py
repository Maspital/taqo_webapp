from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify as Icon
from dash.exceptions import PreventUpdate

from uuid import uuid4

from src.modules import handler, module_cards


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


def add_module_to_pipe(current_pipes, pipe_id, module_id):
    current_pipes.setdefault(pipe_id, [])
    instance_id = str(uuid4())
    new_instance = {
        "module_id": module_id,
        "instance_id": instance_id,
        "parameters": handler.get_default_parameters(module_id),
    }
    action = {"action": "add",
              "pipe_id": pipe_id,
              "index": None,
              "module_id": module_id,
              "instance_id": instance_id}
    current_pipes[pipe_id].append(new_instance)

    return current_pipes, action


def remove_module_from_pipe(current_pipes, instance_id):
    for pipe_id, instances in current_pipes.items():
        for i, instance in enumerate(instances):
            if instance["instance_id"] == instance_id:
                action = {"action": "delete",
                          "pipe_id": pipe_id,
                          "index": i,
                          "module_id": None,
                          "instance_id": instance_id}
                del current_pipes[pipe_id][i]
                # if the pipeline is empty, remove it
                if not current_pipes[pipe_id]:
                    action = {"action": "delete_pipe_empty",
                              "pipe_id": pipe_id,
                              "index": i,
                              "module_id": None,
                              "instance_id": instance_id}
                    del current_pipes[pipe_id]
                return current_pipes, action
    raise PreventUpdate


def move_module_left(current_pipes, pipe_id, instance_id):
    index = None
    for i, module in enumerate(current_pipes[pipe_id]):
        if module["instance_id"] == instance_id:
            index = i
            break
    if index is None or len(current_pipes[pipe_id]) < 2 or index == 0:
        raise PreventUpdate

    action = {"action": "swap",
              "pipe_id": pipe_id,
              "index": [index, index-1],
              "module_id": None,
              "instance_id": instance_id}
    current_pipes[pipe_id][index], current_pipes[pipe_id][index-1] = \
        current_pipes[pipe_id][index-1], current_pipes[pipe_id][index]
    return current_pipes, action


def move_module_right(current_pipes, pipe_id, instance_id):
    index = None
    for i, module in enumerate(current_pipes[pipe_id]):
        if module["instance_id"] == instance_id:
            index = i
            break
    if index is None or len(current_pipes[pipe_id]) < 2 or index == len(current_pipes[pipe_id])-1:
        raise PreventUpdate

    action = {"action": "swap",
              "pipe_id": pipe_id,
              "index": [index, index + 1],
              "module_id": None,
              "instance_id": instance_id}
    current_pipes[pipe_id][index+1], current_pipes[pipe_id][index] = \
        current_pipes[pipe_id][index], current_pipes[pipe_id][index+1]
    return current_pipes, action


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
            width=3,
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
