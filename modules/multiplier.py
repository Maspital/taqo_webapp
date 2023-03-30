def multiply(dataset):
    name = list(dataset.keys())[0]
    for key, value in dataset[name].items():
        dataset[name][key] = value * 2
    return dataset
