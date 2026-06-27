import json

INPUT = "distilled_dataset/train.json"
OUTPUT = "distilled_dataset/train_chat.json"

with open(
    INPUT,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

converted = []

for sample in data:

    converted.append({

        "messages": [

            {
                "role": "user",
                "content":
                    sample["instruction"]
            },

            {
                "role": "assistant",
                "content":
                    sample["output"]
            }

        ]

    })

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        converted,
        f,
        indent=4,
        ensure_ascii=False
    )

print(
    "Converted",
    len(converted),
    "samples."
)