import json


def load_dataset(path):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_sample(dataset, index=0):

    return dataset[index]