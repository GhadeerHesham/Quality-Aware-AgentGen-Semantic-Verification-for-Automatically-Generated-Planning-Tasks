import json
import os
import random


INPUT_FILE = "distilled_dataset/teacher_data.json"
OUTPUT_FILE = "distilled_dataset/quality_teacher_data.json"
TRAIN_FILE = "distilled_dataset/train_quality.json"
VALID_FILE = "distilled_dataset/valid_quality.json"
RANDOM_SEED = 42


def load_teacher_dataset(input_file=INPUT_FILE):
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Teacher dataset not found: {input_file}"
        )

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        dataset = json.load(f)

    if not isinstance(dataset, list):
        raise ValueError(
            "Teacher dataset must be a JSON list."
        )

    print()
    print("Teacher dataset loaded.")
    print("Samples:", len(dataset))

    return dataset


def _looks_like_pddl_request(sample):
    text = (
        sample.get("instruction", "")
        + "\n"
        + sample.get("output", "")
    ).lower()

    return "pddl" in text


def _has_pddl_output(output):
    lowered = output.lower()

    return (
        "```pddl" in lowered
        or "(define" in lowered
    )


def score_teacher_sample(sample):
    score = 100
    reasons = []

    instruction = sample.get("instruction", "")
    output = sample.get("output", "")

    if not sample.get("id"):
        score -= 5
        reasons.append("missing_id")

    if not instruction.strip():
        score -= 35
        reasons.append("missing_instruction")

    if not output.strip():
        score -= 45
        reasons.append("missing_output")

    if output.strip() and len(output.strip()) < 50:
        score -= 20
        reasons.append("output_too_short")

    if _looks_like_pddl_request(sample) and not _has_pddl_output(output):
        score -= 25
        reasons.append("missing_pddl_structure")

    lowered_output = output.lower()

    if (
        "todo" in lowered_output
        or "placeholder" in lowered_output
        or "lorem ipsum" in lowered_output
    ):
        score -= 30
        reasons.append("placeholder_text")

    score = max(score, 0)

    if score >= 80:
        label = "high"
    elif score >= 60:
        label = "medium"
    else:
        label = "low"

    if not reasons:
        reasons.append("passes_basic_quality_checks")

    return score, label, reasons


def build_quality_sample(sample):
    score, label, reasons = score_teacher_sample(sample)

    quality_sample = dict(sample)
    quality_sample["quality_score"] = score
    quality_sample["quality_label"] = label
    quality_sample["quality_reason"] = reasons

    return quality_sample


def save_dataset(dataset, output_file=OUTPUT_FILE):
    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            dataset,
            f,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("Quality dataset saved.")
    print("Samples:", len(dataset))
    print("Output:", output_file)


def split_quality_dataset(
    dataset,
    train_file=TRAIN_FILE,
    valid_file=VALID_FILE,
    train_ratio=0.9
):
    shuffled = list(dataset)

    random.seed(RANDOM_SEED)
    random.shuffle(shuffled)

    split_index = int(
        len(shuffled) * train_ratio
    )

    train_set = shuffled[:split_index]
    valid_set = shuffled[split_index:]

    save_dataset(train_set, train_file)
    save_dataset(valid_set, valid_file)

    print()
    print("Quality dataset split complete.")
    print("Training samples:", len(train_set))
    print("Validation samples:", len(valid_set))


def build_dataset():
    teacher_dataset = load_teacher_dataset()

    quality_dataset = [
        build_quality_sample(sample)
        for sample in teacher_dataset
    ]

    save_dataset(quality_dataset)
    split_quality_dataset(quality_dataset)

    return quality_dataset
