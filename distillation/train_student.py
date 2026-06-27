import argparse
from collections import Counter

try:
    from .student_quality_model import (
        load_json,
        save_json,
        train_model
    )
except ImportError:
    from student_quality_model import (
        load_json,
        save_json,
        train_model
    )


DEFAULT_INPUT_FILE = "distilled_dataset/verified_tasks.json"
DEFAULT_MODEL_FILE = "distilled_model/student_quality_model.json"
DEFAULT_SUMMARY_FILE = "distilled_model/student_training_summary.json"


def train_student(
    input_file=DEFAULT_INPUT_FILE,
    model_file=DEFAULT_MODEL_FILE,
    summary_file=DEFAULT_SUMMARY_FILE
):
    records = load_json(input_file)
    model = train_model(records)

    label_counts = Counter(
        record["decision"]
        for record in records
    )

    summary = {
        "input_file": input_file,
        "model_file": model_file,
        "training_examples": len(records),
        "label_counts": dict(label_counts),
        "vocabulary_size": len(model["vocabulary"]),
        "model_type": model["model_type"]
    }

    save_json(
        model_file,
        model
    )
    save_json(
        summary_file,
        summary
    )

    return summary


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Train a lightweight student quality model "
            "from verified PDDL task labels."
        )
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_FILE
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_FILE
    )
    parser.add_argument(
        "--summary",
        default=DEFAULT_SUMMARY_FILE
    )

    args = parser.parse_args()

    summary = train_student(
        input_file=args.input,
        model_file=args.model,
        summary_file=args.summary
    )

    print()
    print("Student quality model trained.")
    print("Input:", summary["input_file"])
    print("Model:", summary["model_file"])
    print("Training examples:", summary["training_examples"])
    print("Labels:", summary["label_counts"])
    print("Vocabulary size:", summary["vocabulary_size"])


if __name__ == "__main__":
    main()
