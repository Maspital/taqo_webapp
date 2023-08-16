from dash import Output, Input, State, ALL, ctx
from dash.exceptions import PreventUpdate

from src.layout import module_preview
from src.layout import pipelines


def get_callbacks(app):
    @app.callback(
        Output('pipeline_layout', 'children'),
        Output("state_last_action", "data", allow_duplicate=True),
        Input('add_pipeline_button', 'n_clicks'),
        State('pipeline_layout', 'children'),
    )
    def callback_add_pipeline(new_pipe_name, cur_layout):
        return add_pipeline(new_pipe_name, cur_layout)

    @app.callback(
        Output('pipeline_layout', 'children', allow_duplicate=True),
        Output("state_last_action", "data", allow_duplicate=True),
        Input({
            "type": "pipeline_delete_button", "pipe_id_to_delete": ALL
        }, "n_clicks"),
        State('pipeline_layout', 'children'),
    )
    def callback_delete_pipeline(del_button_press_count, cur_layout):
        return delete_pipeline(del_button_press_count, cur_layout)

    @app.callback(
        Output({
            "type": "pipeline_select_dropdown",
            "id": ALL,
        }, "children"),
        Input("pipeline_layout", "children"),
        Input("state_module_ids", "data"),
    )
    def callback_set_dropdown_options(pipes, module_ids):
        return set_dropdown_options(pipes, module_ids)

    @app.callback(
        Output({
            "type": "pipeline_module_row", "id": ALL,
        }, "children"),
        Input("state_last_action", "data"),
        State({
            "type": "pipeline_module_row", "id": ALL,
        }, "children"),
        State({
            "type": "pipeline_module_row", "id": ALL,
        }, "id"),
    )
    def callback_pipes_have_changed(action, current_layout, row_ids):
        return pipes_have_changed(action, current_layout, row_ids)


def add_pipeline(new_pipe_name, cur_layout):
    if new_pipe_name:
        return pipelines.add_pipeline(cur_layout, new_pipe_name), None
    else:
        raise PreventUpdate


def delete_pipeline(del_button_press_count, cur_layout):
    if any(item is not None for item in del_button_press_count):
        # this should only ever be reached if a delete-button has been pressed
        pipe_id = ctx.triggered_id["pipe_id_to_delete"]
        return pipelines.remove_pipeline(cur_layout, pipe_id), None
    else:
        raise PreventUpdate


def set_dropdown_options(pipes, module_ids):
    if pipes:
        return module_preview.set_dropdown_options(pipes, module_ids)
    else:
        return [[] for _ in range(len(module_ids))]


def pipes_have_changed(action, current_layout, row_ids):
    # there are three cases:
    # - a module has been added ["add"]
    # - a module has been deleted ["delete"]
    #       - subcase: it was the last module of the pipe, which is now empty ["delete_pipe_empty"]
    # - a module has been moved (i.e., two modules have been swapped) ["swap"]
    if not action:
        # some changes to the layout might trigger this incorrectly, causing actions to be repeated.
        # within these callbacks, set action to None to prevent this
        raise PreventUpdate

    index = None
    # obtain index of component in layout that changed
    for i, pipe_id in enumerate(row_ids):
        if pipe_id["id"] == action["pipe_id"]:
            index = i
            break
    if index is None:
        raise PreventUpdate

    current_layout = pipelines.modify_layout(current_layout, action, index)

    return current_layout
