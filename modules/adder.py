def add(dataset):
    name = list(dataset.keys())[0]
    print(name)
    for key, value in dataset[name].items():
        dataset[name][key] = value + 1
    print(dataset)
    return dataset
