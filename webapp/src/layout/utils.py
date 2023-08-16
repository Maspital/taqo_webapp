from dash import html


def large_visual_divider():
    divider = html.Hr(
        style={
            "border": "none",
            "borderTop": "10px double #333",
            "color": "#333",
            "overflow": "visible",
            "height": "5px",
        }
    )

    return divider
