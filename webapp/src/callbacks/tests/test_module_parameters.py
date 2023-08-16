# Accessing these private members is suggested by the official dash docs
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash.exceptions import PreventUpdate

from typing import Callable
import json
import pytest
from copy import deepcopy

from src.callbacks.module_parameters import set_num_or_json_parameters, set_string_parameters, check_text_input


def test_set_num_and_json_parameter():
    old_pipeline = {
        "pipe_1": [{
            "module_id": "mod_1",
            "instance_id": "inst_1",
            "parameters": {
                "test_json_param_1": {"hello": "world"},
                "test_num_param_2": 2,
                "test_num_param_3": 3,
            }}]}
    expected_out = deepcopy(old_pipeline)
    expected_out["pipe_1"][0]["parameters"]["test_num_param_2"] = 42

    all_setters = [
        custom_context(module_id="mod_1", instance_id="inst_1", pipe_id="pipe_1", param_name="test_json_param_1",
                       content="JSON"),
        custom_context(module_id="mod_1", instance_id="inst_1", pipe_id="pipe_1", param_name="test_num_param_2",
                       content="NUM"),
        custom_context(module_id="mod_1", instance_id="inst_1", pipe_id="pipe_1", param_name="test_num_param_3",
                       content="NUM")
    ]
    new_pipeline = run_callback(
        set_num_or_json_parameters,
        [
            ['{"hello": "world"}', 42, 3],
            [json.loads(setter) for setter in all_setters],
            old_pipeline
        ],
        [{"prop_id": all_setters[1] + ".value"}],
    )
    assert new_pipeline == expected_out

    expected_out["pipe_1"][0]["parameters"]["test_json_param_1"] = {"hello": "general kenobi"}
    new_pipeline = run_callback(
        set_num_or_json_parameters,
        [
            ['{"hello": "general kenobi"}', 42, 3],
            [json.loads(setter) for setter in all_setters],
            old_pipeline
        ],
        [{"prop_id": all_setters[0] + ".value"}],
    )
    assert new_pipeline == expected_out

    with pytest.raises(PreventUpdate):
        run_callback(
            set_num_or_json_parameters,
            [
                ['{"hello": "general kenobi"}', 42, 3],
                [json.loads(setter) for setter in all_setters],
                old_pipeline
            ],
            [{"prop_id": all_setters[0] + ".value"}],
        )


def test_set_string_parameter():
    old_pipeline = {
        "pipe_1": [{
            "module_id": "mod_1",
            "instance_id": "inst_1",
            "parameters": {
                "test_str_param_1": "this is a string",
                "test_str_param_2": "another string",
            }}]}
    expected_out = deepcopy(old_pipeline)
    expected_out["pipe_1"][0]["parameters"]["test_str_param_2"] = "CAPITAL"

    all_setters = [
        custom_context(module_id="mod_1", instance_id="inst_1", pipe_id="pipe_1", param_name="test_str_param_1",
                       regex=r"^[A-Z]+$", content="STRING"),
        custom_context(module_id="mod_1", instance_id="inst_1", pipe_id="pipe_1", param_name="test_str_param_2",
                       regex=r"^[A-Z]+$", content="STRING"),
    ]
    new_pipeline = run_callback(
        set_string_parameters,
        [
            ["this is a string", "CAPITAL"],
            [json.loads(setter) for setter in all_setters],
            old_pipeline
        ],
        [{"prop_id": all_setters[1] + ".value"}],
    )
    assert new_pipeline == expected_out

    with pytest.raises(PreventUpdate):
        run_callback(
            set_string_parameters,
            [
                ["this is a string", "lowercase"],  # should not match regex and thus not update
                [json.loads(setter) for setter in all_setters],
                old_pipeline
            ],
            [{"prop_id": all_setters[1] + ".value"}],
        )


def test_check_text_input():
    component = {"regex": r"^[A-Z]+$", "error_msg": "Upper case only!"}
    user_input = "CAPITAL"
    desired_out = None

    output = run_callback(
        check_text_input,
        [user_input, component],
        []
    )
    assert output == desired_out

    user_input = "lowercase stuff"
    desired_out = component["error_msg"]
    output = run_callback(
        check_text_input,
        [user_input, component],
        []
    )
    assert output == desired_out


def run_callback(callback_func: Callable, parameters: list, custom_ctx: list[dict]):
    context_value.set(
        AttributeDict(
            **{
                "triggered_inputs": custom_ctx
            }
        )
    )
    return callback_func(*parameters)


def custom_context(module_id, instance_id, pipe_id, param_name, content, regex="qwer", error_msg="qwer"):
    if content == "NUM" or content == "JSON":
        return (
            '{"type":"param_setter",'
            f'"module_id":"{module_id}",'
            f'"instance_id":"{instance_id}",'
            f'"pipe_id":"{pipe_id}",'
            f'"param_name":"{param_name}",'
            f'"content":"{content}"}}'
        )
    if content == "STRING":
        return (
            '{"type":"param_setter",'
            f'"module_id":"{module_id}",'
            f'"instance_id":"{instance_id}",'
            f'"pipe_id":"{pipe_id}",'
            f'"param_name":"{param_name}",'
            f'"regex":"{regex}",'
            f'"error_msg":"{error_msg}",'
            f'"content":"{content}"}}'
        )
