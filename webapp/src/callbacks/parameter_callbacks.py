from dash import Output, Input, State, MATCH, ALL, ctx
from dash.exceptions import PreventUpdate

import re
import json


def get_callbacks(app):
    @app.callback(
        Output("state_pipelines", "data", allow_duplicate=True),
        Input(
            {
                "type": "param_setter",
                "module_id": ALL,
                "instance_id": ALL,
                "pipe_id": ALL,
                "param_name": ALL,
                "content": ALL,
            }, "value"),
        Input(
            {
                "type": "param_setter",
                "module_id": ALL,
                "instance_id": ALL,
                "pipe_id": ALL,
                "param_name": ALL,
                "content": ALL,
            }, "id"),
        State("state_pipelines", "data"),
    )
    def set_num_or_json_parameters(values, ids, current_pipelines):
        trigger = ctx.triggered_id
        if not ctx.triggered_id:
            raise PreventUpdate

        input_index = ids.index(trigger)
        new_value = values[input_index]
        if new_value is None or new_value == "":
            raise PreventUpdate
        
        if trigger["content"] == "json":
            try:
                new_value = json.loads(new_value)
            except json.decoder.JSONDecodeError:
                raise PreventUpdate

        pipe_id = trigger["pipe_id"]
        param_name = trigger["param_name"]
        pipeline = current_pipelines[pipe_id]
        index_to_change = None

        for index, module in enumerate(pipeline):
            if module["instance_id"] == trigger["instance_id"]:
                index_to_change = index
                break
        if index_to_change is None:
            raise PreventUpdate("Attempted to update a parameter that could not be found")
        old_value = current_pipelines[pipe_id][index_to_change]["parameters"][param_name]
        if old_value == new_value:
            raise PreventUpdate

        current_pipelines[pipe_id][index_to_change]["parameters"][param_name] = new_value
        return current_pipelines

    @app.callback(
        Output("state_pipelines", "data", allow_duplicate=True),
        Input(
            {
                "type": "param_setter",
                "module_id": ALL,
                "instance_id": ALL,
                "pipe_id": ALL,
                "param_name": ALL,
                "regex": ALL,
                "error_msg": ALL,
                "content": ALL,
            }, "value"),
        Input(
            {
                "type": "param_setter",
                "module_id": ALL,
                "instance_id": ALL,
                "pipe_id": ALL,
                "param_name": ALL,
                "regex": ALL,
                "error_msg": ALL,
                "content": ALL,
            }, "id"),
        State("state_pipelines", "data"),
    )
    def set_string_parameters(values, ids, current_pipelines):
        trigger = ctx.triggered_id
        if not ctx.triggered_id:
            raise PreventUpdate

        input_index = ids.index(trigger)
        new_value = values[input_index]
        pattern = re.compile(trigger["regex"])
        if not pattern.match(new_value):
            raise PreventUpdate

        pipe_id = trigger["pipe_id"]
        param_name = trigger["param_name"]
        pipeline = current_pipelines[pipe_id]
        index_to_change = None

        for index, module in enumerate(pipeline):
            if module["instance_id"] == trigger["instance_id"]:
                index_to_change = index
                break
        if index_to_change is None:
            raise PreventUpdate("Attempted to update a parameter that could not be found")
        old_value = current_pipelines[pipe_id][index_to_change]["parameters"][param_name]
        if old_value == new_value:
            raise PreventUpdate

        current_pipelines[pipe_id][index_to_change]["parameters"][param_name] = new_value
        return current_pipelines

    @app.callback(
        Output(
            {
                "type": "param_setter",
                "module_id": MATCH,
                "instance_id": MATCH,
                "pipe_id": MATCH,
                "param_name": MATCH,
                "regex": MATCH,
                "error_msg": MATCH,
                "content": MATCH,
            }, "error"),
        Input(
            {
                "type": "param_setter",
                "module_id": MATCH,
                "instance_id": MATCH,
                "pipe_id": MATCH,
                "param_name": MATCH,
                "regex": MATCH,
                "error_msg": MATCH,
                "content": MATCH,
            }, "value"),
        State(
            {
                "type": "param_setter",
                "module_id": MATCH,
                "instance_id": MATCH,
                "pipe_id": MATCH,
                "param_name": MATCH,
                "regex": MATCH,
                "error_msg": MATCH,
                "content": MATCH,
            }, "id"),
    )
    def check_text_input(user_input, component):
        pattern = re.compile(component["regex"])
        if pattern.match(user_input):
            return None
        else:
            return component["error_msg"]
