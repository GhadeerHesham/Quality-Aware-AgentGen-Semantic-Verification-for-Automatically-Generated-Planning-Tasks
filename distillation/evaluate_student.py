import argparse

try:
    from .student_quality_model import (
        evaluate_records,
        load_json,
        predict,
        record_text,
        save_json
    )
except ImportError:
    from student_quality_model import (
        evaluate_records,
        load_json,
        predict,
        record_text,
        save_json
    )


DEFAULT_INPUT_FILE = "distilled_dataset/verified_tasks.json"
DEFAULT_MODEL_FILE = "distilled_model/student_quality_model.json"
DEFAULT_OUTPUT_FILE = "distilled_model/student_evaluation.json"
DEFAULT_PREDICTIONS_FILE = "distilled_model/student_predictions.json"


def evaluate_student(
    input_file=DEFAULT_INPUT_FILE,
    model_file=DEFAULT_MODEL_FILE,
    output_file=DEFAULT_OUTPUT_FILE,
    predictions_file=DEFAULT_PREDICTIONS_FILE
):
    records = load_json(input_file)
    evaluation = evaluate_records(records)
    model = load_json(model_file)

    fitted_predictions = []

    for record in records:
        prediction = predict(
            model,
            record_text(record)
        )

        fitted_predictions.append({
            "id": record["id"],
            "actual_decision": record["decision"],
            "predicted_decision": prediction["decision"],
            "actual_quality_score": record["quality_score"],
            "estimated_quality_score": prediction["estimated_quality_score"],
            "correct": prediction["decision"] == record["decision"]
        })

    evaluation["input_file"] = input_file
    evaluation["model_file"] = model_file
    evaluation["output_file"] = output_file
    evaluation["predictions_file"] = predictions_file
    evaluation["fitted_model_accuracy"] = (
        round(
            sum(
                1
                for item in fitted_predictions
                if item["correct"]
            )
            / len(fitted_predictions),
            4
        )
        if fitted_predictions
        else 0
    )

    save_json(
        output_file,
        evaluation
    )
    save_json(
        predictions_file,
        fitted_predictions
    )

    return evaluation


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate the lightweight student quality model "
            "with leave-one-out validation."
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
        "--output",
        default=DEFAULT_OUTPUT_FILE
    )
    parser.add_argument(
        "--predictions",
        default=DEFAULT_PREDICTIONS_FILE
    )

    args = parser.parse_args()

    evaluation = evaluate_student(
        input_file=args.input,
        model_file=args.model,
        output_file=args.output,
        predictions_file=args.predictions
    )

    print()
    print("Student quality model evaluated.")
    print("Input:", evaluation["input_file"])
    print("Output:", evaluation["output_file"])
    print("Predictions:", evaluation["predictions_file"])
    print("Examples:", evaluation["total_examples"])
    print("Correct:", evaluation["correct"])
    print("Accuracy:", evaluation["accuracy"])
    print("Fitted model accuracy:", evaluation["fitted_model_accuracy"])


if __name__ == "__main__":
    main()
