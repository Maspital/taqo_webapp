from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify as Icon


def create_module_card(module, pipe_id, instance_id):
    required_fields = [
        html.Li(html.Code(field), style={"fontFamily": "monospace"})
        for field in module.required_fields
    ]

    card = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(html.H6(module.title), width="auto"),
                        dbc.Col(submenu(module.id, pipe_id, instance_id), width="auto"),
                    ],
                    justify="between",
                    align="start",
                ),
                html.P(),
                html.P(
                    module.description,
                    className="card-text",
                ),
                html.P(
                    ["Required fields:",
                     html.Ul(required_fields)
                     ],
                    className="card-text",
                ) if required_fields else None,
                param_setter(module, instance_id, pipe_id)
            ],
        ),
        id={
            "type": "module_instance_card",
            "module_id": module.id,
            "pipe_id": pipe_id,
            "instance_id": instance_id,
        }
    )

    return card


def submenu(module_id, pipe_id, instance_id):
    return dbc.ButtonGroup(
        [
            dbc.Button(
                Icon(icon="bi:arrow-left"),
                color="light",
                id={
                    "type": "module_move_left",
                    "module_id": module_id,
                    "pipe_id": pipe_id,
                    "instance_id": instance_id,
                },
            ),
            dbc.Button(
                Icon(icon="bi:trash"),
                color="light",
                id={
                    "type": "module_delete_button",
                    "module_id": module_id,
                    "pipe_id": pipe_id,
                    "instance_id": instance_id,
                },
            ),
            dbc.Button(
                Icon(icon="bi:arrow-right"),
                color="light",
                id={
                    "type": "module_move_right",
                    "module_id": module_id,
                    "pipe_id": pipe_id,
                    "instance_id": instance_id,
                },
            ),
        ],
        size="sm",
    )


def param_setter(module, instance_id, pipe_id):
    if not hasattr(module, "custom_params"):
        return html.P("No parameters for this pipeline.", className="card-text")

    param_setters = []

    for param_name, settings in module.custom_params.items():
        base_settings = get_settings(param_name, settings, module, instance_id, pipe_id)

        if settings["type"] == "SINGLE_NUMBER":
            param_setters.append(dmc.Text(f"{param_name}:"))
            param_setters.append(
                dmc.Slider(**base_settings)
            )
            param_setters.append(html.Br())
        elif settings["type"] == "RANGE":
            param_setters.append(dmc.Text(f"{param_name}:"))
            param_setters.append(
                dmc.RangeSlider(
                    **base_settings,
                    minRange=settings["minRange"] if settings.get("minRange") else 0,
                    maxRange=settings["maxRange"] if settings.get("maxRange") else settings["max"],
                )
            )
            param_setters.append(html.Br())
        elif settings["type"] == "STRING":
            param_setters.append(dmc.TextInput(**base_settings))
        elif settings["type"] == "JSON":
            param_setters.append(dmc.JsonInput(**base_settings))

    return html.Div(param_setters)


def get_settings(param_name, settings, module, instance_id, pipe_id):
    if settings["type"] in ["SINGLE_NUMBER", "RANGE"]:
        return {
            "id": {
                "type": "param_setter",
                "module_id": module.id,
                "instance_id": instance_id,
                "pipe_id": pipe_id,
                "param_name": param_name,
                "content": "number",
            },
            "value": settings["default"],
            "min": settings["min"],
            "max": settings["max"],
            "marks": [
                {"value": settings["min"], "label": settings["min"]},
                {"value": settings["max"], "label": settings["max"]},
            ],
            "step": settings["step"] if settings.get("step") else 1,
            "style": {"paddingBottom": "10px"},
        }
    elif settings["type"] == "STRING":
        return {
            "id": {
                "type": "param_setter",
                "module_id": module.id,
                "instance_id": instance_id,
                "pipe_id": pipe_id,
                "param_name": param_name,
                "regex": settings["regex"],
                "error_msg": settings["error_msg"],
                "content": "string",
            },
            "label": param_name,
            "description": settings["description"],
            "value": settings["default"],
            "debounce": 500,
        }
    elif settings["type"] == "JSON":
        return {
            "id": {
                "type": "param_setter",
                "module_id": module.id,
                "instance_id": instance_id,
                "pipe_id": pipe_id,
                "param_name": param_name,
                "content": "json",
            },
            "label": param_name,
            "validationError": settings["error_msg"] if settings.get("error_msg") else None,
            "value": settings["default"],
            "placeholder": settings["placeholder"] if settings.get("placeholder") else None,
            "minRows": 4,
            "autosize": False,
            "formatOnBlur": True,
            "debounce": 500,
        }
