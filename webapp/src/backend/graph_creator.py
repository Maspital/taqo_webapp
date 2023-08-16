import plotly.graph_objs as go

from typing import Tuple


def add_simple_trace(current_fig: go.Figure, dataset: dict, x_axis: str, y_axis: str) -> go.Figure:
    for full_pipe_id, data in dataset.items():
        pipeline_name = full_pipe_id.split(".")[1]

        current_fig.add_trace(
            go.Scatter(
                x=data[x_axis],
                y=data[y_axis],
                line={"width": 3},
                name=pipeline_name,
            )
        )

    return current_fig


def create_custom_chart(new_chart: dict, data: dict) -> go.Figure:
    fig = go.Figure()
    graph_title = "Nothing here yet..."
    x_axis, y_axis = select_data_for_axis(new_chart["x_axis"], new_chart["y_axis"])

    # add traces here depending on settings
    if data:
        # source is the same for all pipes
        graph_title = ", ".join(list(data.values())[0]["metadata"]["used_source"])
        fig = add_simple_trace(fig, data, x_axis, y_axis)

    fig.update_layout(
        xaxis_title=data_x().get(new_chart["x_axis"]),
        yaxis_title=data_y().get(new_chart["y_axis"]),
        title={
            "text": graph_title,
            "xanchor": "center",
            "yanchor": "top",
            "y": 0.9,
            "x": 0.5,
        },
    )
    fig.update_xaxes(autorange=True)
    if data:
        fig.update_yaxes(range=get_y_range(data, y_axis))
    else:
        fig.update_yaxes(autorange=True)

    return fig


def data_x():
    return {
        "num_sres_weighted": "Viewed SREs",
        "list_risk_scores": "Risk Scores",
    }


def data_y():
    return {
        "num_tps_weighted": "Average Viewed True Positives (TPs)",
        "num_fps_weighted": "Average Viewed False Positives (FPs)",
        "num_techs_weighted": "Average Viewed Unique Techniques",
    }


def select_data_for_axis(x_axis: str, y_axis: str) -> Tuple[str, str]:
    """
    Rudimentary solution for ensuring data length matches up.
    We will likely have to revisit this at some point.
    """
    if x_axis == "num_sres_weighted":
        # use set with added (0,0) point
        return x_axis + "_extended", y_axis + "_extended"
    elif x_axis == "list_risk_scores":
        # use set without added (0,0) point, wouldn't make sense when mapping to risk scores
        return x_axis, y_axis
    else:
        # if none of these match, just return the original to ensure tests can fail properly
        return x_axis, y_axis


def get_y_range(data, y_axis):
    maximum = 0
    for dataset in data.values():
        cur_max = max(dataset[y_axis])
        maximum = cur_max if cur_max > maximum else maximum
    min_range = -maximum*0.05
    max_range = maximum + maximum*0.05
    return [min_range, max_range]
