# Accessing these private members is suggested by the official dash docs
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash.exceptions import PreventUpdate
import dash_bootstrap_components

from typing import Callable
import pytest
from mock import patch

from src.callbacks.graph_layout import toggle_modal, add_or_remove_graph, update_charts


def test_toggle_modal():
    original_state = True
    assert original_state is toggle_modal(None, None, original_state)
    assert original_state is not toggle_modal(1, None, original_state)


@patch("src.callbacks.graph_layout.add_graph")
def test_graph_added(mock_add_func):
    old_state = {}
    new_state = {
        "graph_1": {
            "x_axis": "some_x1", "y_axis": "some_y3", "options": {},
        }}
    run_callback(
        add_or_remove_graph,
        [new_state, old_state, None, None],
        [],
    )
    assert mock_add_func.called


@patch("src.callbacks.graph_layout.delete_graph")
def test_graph_removed(mock_delete_func):
    old_state = {
        "graph_1": {
            "x_axis": "some_x1", "y_axis": "some_y3", "options": {},
        }}
    new_state = {}
    run_callback(
        add_or_remove_graph,
        [new_state, old_state, None, None],
        [],
    )
    assert mock_delete_func.called


def test_no_change_on_same_state():
    old_state = {
        "graph_1": {
            "x_axis": "some_x1", "y_axis": "some_y3", "options": {},
        }}
    new_state = old_state
    with pytest.raises(PreventUpdate):
        run_callback(
            add_or_remove_graph,
            [new_state, old_state, None, None],
            [],
        )


def test_update_charts():
    graphs_to_render = {
        "graph_1": {
            "x_axis": "some_x1", "y_axis": "some_y3", "options": {},
        },
        "graph_2": {
            "x_axis": "some_x2", "y_axis": "some_y3", "options": {},
        },
    }
    generated_layout = run_callback(
        update_charts,
        [None, graphs_to_render],
        []
    )
    assert len(generated_layout) == 2
    assert all(isinstance(element, dash_bootstrap_components._components.Col)
               for element in generated_layout)

    with pytest.raises(PreventUpdate):
        run_callback(
            update_charts,
            [None, None],
            []
        )


def run_callback(callback_func: Callable, parameters: list, custom_context: list[dict]):
    context_value.set(
        AttributeDict(
            **{
                "triggered_inputs": custom_context
            }
        )
    )
    return callback_func(*parameters)
