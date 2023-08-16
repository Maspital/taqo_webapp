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


def param_setter(module, instance_id: str, pipe_id: str) -> html:
    if not hasattr(module, "custom_params"):
        return html.P("No parameters for this pipeline.", className="card-text")

    param_setters = []

    for param_name, settings in module.custom_params.items():
        setter_id = get_base_id(
            module_id=module.id,
            instance_id=instance_id,
            pipe_id=pipe_id,
            param_name=param_name,
            content=settings["type"],
        )
        setting = get_settings(param_name, settings, setter_id)

        if settings["type"] == "SINGLE_NUMBER":
            param_setters.append(dmc.Text(f"{param_name}:"))
            param_setters.append(dmc.Slider(**setting))
        elif settings["type"] == "RANGE":
            param_setters.append(dmc.Text(f"{param_name}:"))
            param_setters.append(dmc.RangeSlider(**setting))
        elif settings["type"] == "STRING":
            param_setters.append(dmc.TextInput(**setting))
        elif settings["type"] == "JSON":
            param_setters.append(dmc.JsonInput(**setting))
        elif settings["type"] == "RADIO":
            param_setters.append(dmc.Text(f"{param_name}:"))
            param_setters.append(dbc.RadioItems(**setting))
        elif settings["type"] == "CHECKLIST":
            param_setters.append(dmc.Text(f"{param_name}:"))
            param_setters.append(dbc.Checklist(**setting))

        param_setters.append(html.Br())

    if param_setters:
        # Remove the last Br
        param_setters.pop()
    return html.Div(param_setters)


def get_settings(param_name: str, settings: dict, setter_id: dict) -> dict:
    if settings["type"] == "SINGLE_NUMBER":
        return {
            "id": setter_id,
            "value": settings["default"],
            "min": settings["min"],
            "max": settings["max"],
            "marks": [
                {"value": settings["min"], "label": settings["min"]},
                {"value": settings["max"], "label": settings["max"]},
            ],
            "step": settings.get("step", 1),
            "style": {"paddingBottom": "10px"},
        }
    elif settings["type"] == "RANGE":
        return {
            "id": setter_id,
            "value": settings["default"],
            "min": settings["min"],
            "max": settings["max"],
            "minRange": settings.get("minRange", 0),
            "maxRange": settings.get("maxRange", settings["max"]),
            "marks": [
                {"value": settings["min"], "label": settings["min"]},
                {"value": settings["max"], "label": settings["max"]},
            ],
            "step": settings.get("step", 1),
            "style": {"paddingBottom": "10px"},
        }
    elif settings["type"] == "STRING":
        setter_id["error_msg"] = settings["error_msg"]
        setter_id["regex"] = settings["regex"]
        return {
            "id": setter_id,
            "label": param_name,
            "description": settings["description"],
            "value": settings["default"],
            "debounce": 500,
        }
    elif settings["type"] == "JSON":
        return {
            "id": setter_id,
            "label": param_name,
            "validationError": settings.get("error_msg", None),
            "value": settings["default"],
            "placeholder": settings.get("placeholder", None),
            "minRows": 4,
            "autosize": False,
            "formatOnBlur": True,
            "debounce": 500,
        }
    elif settings["type"] == "RADIO" or settings["type"] == "CHECKLIST":
        return {
            "id": setter_id,
            "options": settings["options"],
            "value": settings["default"],
        }


def get_base_id(module_id, instance_id, pipe_id, param_name, content):
    return {
        "type": "param_setter",
        "module_id": module_id,
        "instance_id": instance_id,
        "pipe_id": pipe_id,
        "param_name": param_name,
        "content": content,
    }
