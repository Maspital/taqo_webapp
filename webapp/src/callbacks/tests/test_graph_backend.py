# Accessing these private members is suggested by the official dash docs
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash.exceptions import PreventUpdate

from typing import Callable
import pytest
from mock import patch
from copy import deepcopy

from src.callbacks.graph_backend import add_graph_to_state, remove_graph_from_state


def test_graph_not_added_without_click():
    old_state = {"old_graph_id": {
        "x_axis": "some_x1", "y_axis": "some_y1", "options": {},
    }},

    with pytest.raises(PreventUpdate):
        run_callback(
            add_graph_to_state,
            [
                None,  # n_clicks is none, aka the button has just been initialized, not pressed
                old_state,
                "some_x2",
                "some_y2",
            ],
            [],
        )


@patch("src.callbacks.graph_backend.uuid4")
def test_graph_added_on_click(mocked_uuid4):
    mocked_uuid4.return_value = "new_graph_id"
    old_state = {"old_graph_id": {
        "x_axis": "some_x1", "y_axis": "some_y1", "options": {},
    }}
    expected_new_state = deepcopy(old_state)
    expected_new_state["new_graph_id"] = {
        "x_axis": "some_x2", "y_axis": "some_y2", "options": {},
    }

    output = run_callback(
        add_graph_to_state,
        [
            1,  # n_clicks as if the button has been pressed
            old_state,
            "some_x2",
            "some_y2",
        ],
        [],
    )
    assert output == expected_new_state


def test_graph_not_deleted_without_click():
    old_state = {
        "graph_1": {
            "x_axis": "some_x1", "y_axis": "some_y3", "options": {},
        }
    }

    with pytest.raises(PreventUpdate):
        run_callback(
            remove_graph_from_state,
            [
                [None, None, None],  # all values are None -> no button has been pressed, so dont delete
                old_state,
            ],
            [{"prop_id": '{"type":"delete_graph_button","graph_to_delete":"graph_1"}.n_clicks'}],
        )


def test_graph_deleted_on_click():
    old_state = {
        "graph_1": {
            "x_axis": "some_x1", "y_axis": "some_y3", "options": {},
        },
        "graph_2": {
            "x_axis": "some_x2", "y_axis": "some_y3", "options": {},
        },
        "graph_3": {
            "x_axis": "some_x3", "y_axis": "some_y3", "options": {},
        },
    }
    expected_new_state = deepcopy(old_state)
    del expected_new_state["graph_2"]

    output = run_callback(
        remove_graph_from_state,
        [
            [None, 1, None],  # position of "1" should correspond to position of graph to delete
            old_state,
        ],
        [{"prop_id": '{"type":"delete_graph_button","graph_to_delete":"graph_2"}.n_clicks'}],
    )
    assert output == expected_new_state


def run_callback(callback_func: Callable, parameters: list, custom_context: list[dict]):
    context_value.set(
        AttributeDict(
            **{
                "triggered_inputs": custom_context
            }
        )
    )
    return callback_func(*parameters)
