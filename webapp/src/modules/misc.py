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


def move_sanity_check(new_n_clicks, old_n_clicks):
    # checks if a mv left/right of a module object should be performed

    if not new_n_clicks:
        # no elements currently exist, so dont attempt to move
        return False
    if len(new_n_clicks) != len(old_n_clicks):
        # unequal amounts of objects, meaning either an add or remove has been performed
        return False

    old_sum = sum(num for num in old_n_clicks if num is not None)
    new_sum = sum(num for num in new_n_clicks if num is not None)
    if old_sum == new_sum:
        # equal status of objects, meaning callback triggered incorrectly
        # we cannot just check for equal lists since the order within a list might change
        return False

    return True
