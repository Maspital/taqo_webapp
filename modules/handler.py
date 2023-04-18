import os
import importlib.util
import inspect


def get_datasets():
    dataset_dir = "./datasets/"

    datasets = []
    for path in os.listdir(dataset_dir):
        if os.path.isfile(os.path.join(dataset_dir, path)):
            datasets.append(dataset_dir + path)

    return datasets


def get_pipelines(directory):
    """
    Load all classes from Python modules in a directory.
    Each module represents a category, each class within that module a pipeline of that category.

    :param directory: str, the path to the directory to search for modules.
    :return: dict, categories as keys, list of instantiated classes (pipelines) as values for each ke
    """
    result = {}

    files = os.listdir(directory)

    for file_name in files:
        if not file_name.endswith('.py'):
            continue

        module_path = os.path.join(directory, file_name)

        module_spec = importlib.util.spec_from_file_location(file_name[:-3], module_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        # Get the module's category and classes
        category = getattr(module, 'CATEGORY', None)
        classes = [obj for name, obj in inspect.getmembers(module) if inspect.isclass(obj)]

        # Instantiate the classes and add them to the result dictionary
        if category and classes:
            if category not in result:
                result[category] = []
            for cls in classes:
                instance = cls()
                result[category].append(instance)

    return result
