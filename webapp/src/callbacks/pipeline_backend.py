import dash
from dash import Output, Input, State, ALL, ctx
from dash.exceptions import PreventUpdate

from src.backend import pipelines


def get_callbacks(app):
    @app.callback(
        Output("state_selected_datasets", "data"),
        Input({
            "type": "dataset_select_checkbox", "index": ALL
        }, "checked"),
    )
    def callback_set_current_datasets(checkbox_state):
        return set_current_datasets(checkbox_state)

    @app.callback(
        Output("state_pipelines", "data", allow_duplicate=True),
        Input({
            "type": "pipeline_delete_button", "pipe_id_to_delete": ALL
        }, "n_clicks"),
        State("state_pipelines", "data"),
    )
    def callback_delete_pipeline(del_button_press_count, current_pipelines):
        return delete_pipeline(del_button_press_count, current_pipelines)

    @app.callback(
        Output("state_pipelines", "data", allow_duplicate=True),
        Output("state_last_action", "data", allow_duplicate=True),
        Input({
            "type": "pipeline_select_dropdown_button", "pipe_id": ALL, "module_id": ALL,
        }, "n_clicks"),
        State("state_pipelines", "data"),
    )
    def callback_add_module_to_pipe(_, current_pipelines):
        return add_module_to_pipe(_, current_pipelines)

    @app.callback(
        Output("state_pipelines", "data", allow_duplicate=True),
        Output("state_last_action", "data", allow_duplicate=True),
        Input({
                "type": "module_delete_button",
                "module_id": ALL,
                "pipe_id": ALL,
                "instance_id": ALL,
            }, "n_clicks"),
        State("state_pipelines", "data"),
    )
    def callback_remove_module_from_pipe(n_clicks, current_pipelines):
        return remove_module_from_pipe(n_clicks, current_pipelines)

    @app.callback(
        Output("state_pipelines", "data", allow_duplicate=True),
        Output("state_last_action", "data", allow_duplicate=True),
        Output("state_mv_left_n_clicks", "data", allow_duplicate=True),
        Input(
            {
                "type": "module_move_left",
                "module_id": ALL,
                "pipe_id": ALL,
                "instance_id": ALL,
            }, "n_clicks"),
        State("state_mv_left_n_clicks", "data"),
        State("state_pipelines", "data"),
    )
    def callback_move_module_left(new_n_clicks, old_n_clicks, current_pipelines):
        return move_module_left(new_n_clicks, old_n_clicks, current_pipelines)

    @app.callback(
        Output("state_pipelines", "data", allow_duplicate=True),
        Output("state_last_action", "data", allow_duplicate=True),
        Output("state_mv_right_n_clicks", "data", allow_duplicate=True),
        Input(
            {
                "type": "module_move_right",
                "module_id": ALL,
                "pipe_id": ALL,
                "instance_id": ALL,
            }, "n_clicks"),
        State("state_mv_right_n_clicks", "data"),
        State("state_pipelines", "data"),
    )
    def callback_move_module_right(new_n_clicks, old_n_clicks, current_pipelines):
        return move_module_right(new_n_clicks, old_n_clicks, current_pipelines)


def set_current_datasets(checkbox_state):
    # List items are conveniently ordered by the index of the checkboxes
    selected_dataset_indexes = []
    for index, state in enumerate(checkbox_state):
        if state:
            selected_dataset_indexes.append(index)
    return selected_dataset_indexes


def delete_pipeline(del_button_press_count, current_pipelines):
    if any(item is not None for item in del_button_press_count):
        # this should only ever be reached if a delete-button has been pressed
        pipe_id = ctx.triggered_id["pipe_id_to_delete"]
        if pipe_id in current_pipelines:
            del current_pipelines[pipe_id]
        return current_pipelines
    else:
        raise PreventUpdate


def add_module_to_pipe(_, current_pipelines):
    # Adding a new pipeline also recreates all buttons, which triggers this callback.
    # The condition below prevents that from happening
    if not ctx.triggered or ctx.triggered[0]["value"] is None:
        raise PreventUpdate
    pipe_id = ctx.triggered_id["pipe_id"]
    module_id = ctx.triggered_id["module_id"]

    new_pipelines, action = pipelines.add_module_to_pipe(current_pipelines, pipe_id, module_id)
    return new_pipelines, action


def remove_module_from_pipe(n_clicks, current_pipelines):
    if not n_clicks or all(item is None for item in n_clicks):
        raise PreventUpdate
    instance_id = ctx.triggered_id["instance_id"]

    current_pipelines, new_action = pipelines.remove_module_from_pipe(current_pipelines, instance_id)
    return current_pipelines, new_action


def move_module_left(new_n_clicks, old_n_clicks, current_pipelines):
    if not pipelines.move_sanity_check(new_n_clicks, old_n_clicks):
        return dash.no_update, dash.no_update, new_n_clicks
    pipe_id = ctx.triggered_id["pipe_id"]
    instance_id = ctx.triggered_id["instance_id"]

    try:
        current_pipelines, new_action = pipelines.move_module_left(current_pipelines, pipe_id, instance_id)
    except PreventUpdate:
        return dash.no_update, dash.no_update, new_n_clicks
    return current_pipelines, new_action, new_n_clicks


def move_module_right(new_n_clicks, old_n_clicks, current_pipelines):
    if not pipelines.move_sanity_check(new_n_clicks, old_n_clicks):
        return dash.no_update, dash.no_update, new_n_clicks
    pipe_id = ctx.triggered_id["pipe_id"]
    instance_id = ctx.triggered_id["instance_id"]

    try:
        current_pipelines, new_action = pipelines.move_module_right(current_pipelines, pipe_id, instance_id)
    except PreventUpdate:
        return dash.no_update, dash.no_update, new_n_clicks
    return current_pipelines, new_action, new_n_clicks
