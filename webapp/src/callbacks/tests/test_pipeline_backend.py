# Accessing these private members is suggested by the official dash docs
import dash
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash.exceptions import PreventUpdate

from typing import Callable
import pytest
from mock import patch
from copy import deepcopy

from src.callbacks.pipeline_backend import (
    set_current_datasets,
    delete_pipeline,
    add_module_to_pipe,
    remove_module_from_pipe,
    move_module_left,
    move_module_right,
)


def test_set_current_datasets():
    selected_checkboxes = [True, False, True]
    expected_out = [0, 2]

    actual_out = run_callback(
        set_current_datasets,
        [selected_checkboxes],
        []
    )
    assert actual_out == expected_out


def test_delete_pipeline():
    old_pipelines = {"pipe_1": "pipe content here", "pipe_2": "pipe content here"}
    expected_out = deepcopy(old_pipelines)
    del expected_out["pipe_2"]

    new_pipelines = run_callback(
        delete_pipeline,
        [[None, 1], old_pipelines],
        [{"prop_id": '{"type":"pipeline_delete_button","pipe_id_to_delete":"pipe_2"}.n_clicks'}],
    )
    assert new_pipelines == expected_out

    with pytest.raises(PreventUpdate):
        run_callback(
            delete_pipeline,
            [[None, None, None], old_pipelines],
            [{"prop_id": '{"type":"pipeline_delete_button","pipe_id_to_delete":"pipe_1"}.n_clicks'}],
        )


@patch("src.callbacks.pipeline_backend.pipelines.add_module_to_pipe")
def test_add_module_to_pipe(mocked_add_func):
    mocked_add_func.return_value = ["", ""]
    run_callback(
        add_module_to_pipe,
        [0, {}],
        [{"prop_id": '{"type":"pipeline_select_dropdown_button","pipe_id":"pipe_1","module_id":"mod_1"}.n_clicks',
          "value": "not none"}],
    )
    assert mocked_add_func.called

    with pytest.raises(PreventUpdate):
        run_callback(
            add_module_to_pipe,
            [0, {}],
            [{"prop_id": '{"type":"pipeline_select_dropdown_button","pipe_id":"pipe_1","module_id":"mod_1"}.n_clicks',
              "value": None}],
        )


def test_remove_module_from_pipe():
    old_pipelines = {"pipe_1": [
        {"instance_id": "inst_1", "module_id": "mod_1"},
        {"instance_id": "inst_2", "module_id": "mod_2"}]}
    expected_out = deepcopy(old_pipelines)
    expected_action = {"action": "delete",
                       "pipe_id": "pipe_1",
                       "index": 0,
                       "module_id": None,
                       "instance_id": "inst_1"}
    del expected_out["pipe_1"][0]

    new_pipelines, new_action = run_callback(
        remove_module_from_pipe,
        [[1, None], old_pipelines],
        [{"prop_id": '{"type":"module_delete_button","instance_id":"inst_1"}.n_clicks'}],
    )
    assert new_pipelines == expected_out
    assert new_action == expected_action

    del expected_out["pipe_1"]
    expected_action = {"action": "delete_pipe_empty",
                       "pipe_id": "pipe_1",
                       "index": 0,
                       "module_id": None,
                       "instance_id": "inst_2"}
    new_pipelines, new_action = run_callback(
        remove_module_from_pipe,
        [[1], old_pipelines],
        [{"prop_id": '{"type":"module_delete_button","instance_id":"inst_2"}.n_clicks'}],
    )
    assert new_pipelines == expected_out
    assert new_action == expected_action

    with pytest.raises(PreventUpdate):
        run_callback(
            delete_pipeline,
            [[None, None, None], old_pipelines],
            [{"prop_id": '{"type":"module_delete_button","instance_id":"instance_1"}.n_clicks'}],
        )


def test_move_module_left():
    old_pipelines = {
        "pipe_1": [
            {"instance_id": "inst_1", "module_id": "mod_1"},
            {"instance_id": "inst_2", "module_id": "mod_1"}],
        "pipe_2": [
            {"instance_id": "inst_3", "module_id": "mod_1"},
            {"instance_id": "inst_4", "module_id": "mod_2"}]}
    expected_out = {
        "pipe_1": [
            {"instance_id": "inst_1", "module_id": "mod_1"},
            {"instance_id": "inst_2", "module_id": "mod_1"}],
        "pipe_2": [
            {"instance_id": "inst_4", "module_id": "mod_2"},
            {"instance_id": "inst_3", "module_id": "mod_1"}]}
    expected_action = {"action": "swap",
                       "pipe_id": "pipe_2",
                       "index": [1, 0],
                       "module_id": None,
                       "instance_id": "inst_4"}

    new_pipelines, action, _ = run_callback(
        move_module_left,
        [[1, 1, 1, 2], [1, 1, 1, 1], old_pipelines],
        [{"prop_id": '{"type":"module_move_left","pipe_id":"pipe_2","instance_id":"inst_4"}.n_clicks'}],
    )
    assert new_pipelines == expected_out
    assert action == expected_action

    expected_out = dash.no_update
    expected_action = dash.no_update
    # instance is already leftmost and cannot be moved further left
    new_pipelines, action, _ = run_callback(
        move_module_left,
        [[1, 1, 3, 1], [1, 1, 2, 1], new_pipelines],
        [{"prop_id": '{"type":"module_move_left","pipe_id":"pipe_2","instance_id":"inst_4"}.n_clicks'}],
    )
    assert new_pipelines == expected_out
    assert action == expected_action


def test_move_module_right():
    old_pipelines = {
        "pipe_1": [
            {"instance_id": "inst_1", "module_id": "mod_1"},
            {"instance_id": "inst_2", "module_id": "mod_1"}],
        "pipe_2": [
            {"instance_id": "inst_3", "module_id": "mod_1"},
            {"instance_id": "inst_4", "module_id": "mod_2"}]}
    expected_out = {
        "pipe_1": [
            {"instance_id": "inst_1", "module_id": "mod_1"},
            {"instance_id": "inst_2", "module_id": "mod_1"}],
        "pipe_2": [
            {"instance_id": "inst_4", "module_id": "mod_2"},
            {"instance_id": "inst_3", "module_id": "mod_1"}]}
    expected_action = {"action": "swap",
                       "pipe_id": "pipe_2",
                       "index": [0, 1],
                       "module_id": None,
                       "instance_id": "inst_3"}

    new_pipelines, action, _ = run_callback(
        move_module_right,
        [[1, 1, 2, 1], [1, 1, 1, 1], old_pipelines],
        [{"prop_id": '{"type":"module_move_left","pipe_id":"pipe_2","instance_id":"inst_3"}.n_clicks'}],
    )
    assert new_pipelines == expected_out
    assert action == expected_action

    expected_out = dash.no_update
    expected_action = dash.no_update
    # instance is already rightmost and cannot be moved further right
    new_pipelines, action, _ = run_callback(
        move_module_right,
        [[1, 1, 1, 3], [1, 1, 1, 2], new_pipelines],
        [{"prop_id": '{"type":"module_move_left","pipe_id":"pipe_2","instance_id":"inst_3"}.n_clicks'}],
    )
    assert new_pipelines == expected_out
    assert action == expected_action


def run_callback(callback_func: Callable, parameters: list, custom_context: list[dict]):
    context_value.set(
        AttributeDict(
            **{
                "triggered_inputs": custom_context
            }
        )
    )
    return callback_func(*parameters)
