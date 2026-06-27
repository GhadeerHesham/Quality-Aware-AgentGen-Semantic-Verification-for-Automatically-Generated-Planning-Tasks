import json
import os

INPUT_FILE = (
    "AgentGen-main/src/data/sft_data.json"
)

OUTPUT_DIR = "distilled_dataset"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "teacher_data.json"
)


def prepare_dataset():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        dataset = json.load(f)

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    teacher_dataset = []

    for sample in dataset:

        teacher_dataset.append({

            "id":
                sample["id"],

            "instruction":
                sample["conversations"][0]["value"],

            "output":
                sample["conversations"][1]["value"]

        })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            teacher_dataset,
            f,
            indent=4,
            ensure_ascii=False
        )

    print()

    print(
        "Teacher dataset created."
    )

    print(
        "Samples:",
        len(teacher_dataset)
    )


if __name__ == "__main__":

    prepare_dataset()