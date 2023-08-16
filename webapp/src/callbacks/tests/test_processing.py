from src.callbacks.processing_callbacks import process_data, dp
from mock import patch


def test_no_trigger_on_missing_input():
    output_missing_data = process_data("Some pipeline state", None)
    output_missing_pipe = process_data(None, "Some data indexes")
    output_missing_both = process_data(None, None)

    assert not any([output_missing_data, output_missing_pipe, output_missing_both])


@patch.object(dp, "execute_pipelines")
def test_execute_pipelines_called(mock_execute_pipelines):
    pipelines = "Some pipeline state"
    dataset_indexes = "Some data indexes"
    process_data(pipelines, dataset_indexes)

    assert mock_execute_pipelines.called
