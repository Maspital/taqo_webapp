from mock import patch
from copy import deepcopy

from src.backend.pipelines import add_module_to_pipe


# remember that patch decorator applies patches from the BOTTOM up
@patch("src.backend.pipelines.uuid4")
@patch("src.backend.pipelines.handler.get_default_parameters")
def test_add_module_to_pipe(mocked_params, mocked_uuid4):
    mocked_uuid4.return_value = "inst_2"
    mocked_params.return_value = {"param_name": "param_value"}
    old_pipelines = {
        "pipe_1": [
            {
                "module_id": "mod_1",
                "instance_id": "inst_1",
                "parameters": {}
            },
        ]
    }
    expected_out = deepcopy(old_pipelines)
    expected_out["pipe_1"].append(
        {"module_id": "mod_2",
         "instance_id": "inst_2",
         "parameters": {"param_name": "param_value"},
         }
    )
    actual_out, _ = add_module_to_pipe(old_pipelines, "pipe_1", "mod_2")
    assert actual_out == expected_out
