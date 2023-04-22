import plotly.graph_objs as go


def create_bar_chart(dataset):
    fig = go.Figure()

    for category_index, (category, data) in enumerate(dataset.items()):
        tp_count = data["tp_count"]
        fp_count = data["fp_count"]

        fig.add_trace(
            go.Bar(
                name=category,
                x=["TPs", "FPs"],
                y=[tp_count, fp_count],
            )
        )

    fig.update_layout(
        dict(
            title="Some title for a graph"
        ),
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        )
    )

    return fig
