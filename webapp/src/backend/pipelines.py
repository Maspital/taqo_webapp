from dash.exceptions import PreventUpdate

from uuid import uuid4

from src.backend import handler


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


def move_sanity_check(new_n_clicks, old_n_clicks):
    # checks if a mv left/right of a module object should be performed

    if not new_n_clicks:
        # no elements currently exist, so don't attempt to move
        return False
    if len(new_n_clicks) != len(old_n_clicks):
        # unequal amounts of objects, meaning either an add or remove has been performed, so don't attempt to move
        return False

    old_sum = sum(num for num in old_n_clicks if num is not None)
    new_sum = sum(num for num in new_n_clicks if num is not None)
    if old_sum == new_sum:
        # equal status of objects, meaning callback triggered incorrectly
        # we cannot just check for equal lists since the order within a list might change
        return False

    return True
