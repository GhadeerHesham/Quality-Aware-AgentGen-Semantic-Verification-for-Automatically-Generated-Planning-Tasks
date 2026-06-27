import json
import random
import os

INPUT_FILE = (
    "distilled_dataset/teacher_data.json"
)

TRAIN_FILE = (
    "distilled_dataset/train.json"
)

VALID_FILE = (
    "distilled_dataset/valid.json"
)

RANDOM_SEED = 42


def split_dataset():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        dataset = json.load(f)

    random.seed(
        RANDOM_SEED
    )

    random.shuffle(
        dataset
    )

    split_index = int(
        len(dataset) * 0.9
    )

    train_set = dataset[:split_index]

    valid_set = dataset[split_index:]

    with open(
        TRAIN_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            train_set,
            f,
            indent=4,
            ensure_ascii=False
        )

    with open(
        VALID_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            valid_set,
            f,
            indent=4,
            ensure_ascii=False
        )

    print()

    print("Dataset split complete.")

    print(
        "Training samples:",
        len(train_set)
    )

    print(
        "Validation samples:",
        len(valid_set)
    )


if __name__ == "__main__":

    split_dataset()