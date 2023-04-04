def add(dataset):
    name = list(dataset.keys())[0]
    for key, value in dataset[name].items():
        dataset[name][key] = value + 1
    return dataset
