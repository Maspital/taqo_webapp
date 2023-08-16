import importlib.util
import inspect
import json

from src.backend.utils import get_webapp_root


def get_datasets() -> list[dict]:
    dataset_json = get_webapp_root() / "config/datasets.json"

    with open(dataset_json, "r") as file:
        datasets = json.load(file)

    return datasets


def get_modules() -> list[any]:
    # Grabs all .py files from the modules directory and instantiates their classes,
    # which are then used for displaying information from that class (aka module) or
    # executing the modules processing function with some given data
    result = []
    module_dir = get_webapp_root() / "modules"

    files = list(module_dir.glob("*.py"))

    for file_name in files:
        module_path = module_dir / file_name

        module_spec = importlib.util.spec_from_file_location(file_name.stem, module_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        # second condition prevents classes imported by the module from being added
        classes = [obj for name, obj in inspect.getmembers(module)
                   if inspect.isclass(obj) and obj.__module__ == module.__name__]

        if classes:
            for cls in classes:
                instance = cls()
                result.append(instance)

    return result


def get_module_ids() -> list[str]:
    modules = get_modules()
    ids = []
    for module in modules:
        ids.append(module.id)
    return ids


def get_modules_as_dict() -> dict[any]:
    modules = get_modules()
    result = {}
    for module in modules:
        result[module.id] = module
    return result


def get_default_parameters(module_id):
    module = get_modules_as_dict()[module_id]
    if not hasattr(module, "custom_params"):
        return None
    params = module.custom_params
    if not params:
        return None

    default = {}
    for param_name, settings in params.items():
        if settings["type"] == "JSON":
            try:
                default[param_name] = json.loads(settings["default"])
            except json.decoder.JSONDecodeError:
                default[param_name] = {}
        else:
            default[param_name] = settings["default"]

    return default
