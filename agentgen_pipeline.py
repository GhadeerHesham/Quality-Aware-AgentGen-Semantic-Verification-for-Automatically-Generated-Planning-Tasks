import argparse
import json
import os

from verifier.task_filter import filter_task


DEFAULT_INPUT_FILE = "generated_tasks.json"
DEFAULT_OUTPUT_FILE = "generated_tasks_quality_report.json"
DEFAULT_THRESHOLD = 80


def load_generated_tasks(input_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Generated task file not found: {input_file}"
        )

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        tasks = json.load(f)

    if not isinstance(tasks, list):
        raise ValueError(
            "Generated task file must contain a JSON list."
        )

    return tasks


def process_generated_task(task, threshold=DEFAULT_THRESHOLD):
    task_id = task.get("id", "unknown-task")
    domain_file = task.get("domain_file")
    problem_file = task.get("problem_file")

    if not domain_file or not problem_file:
        return {
            "id": task_id,
            "domain_file": domain_file,
            "problem_file": problem_file,
            "decision": "REJECT",
            "error": "missing_domain_or_problem_file"
        }

    if not os.path.exists(domain_file):
        return {
            "id": task_id,
            "domain_file": domain_file,
            "problem_file": problem_file,
            "decision": "REJECT",
            "error": "domain_file_not_found"
        }

    if not os.path.exists(problem_file):
        return {
            "id": task_id,
            "domain_file": domain_file,
            "problem_file": problem_file,
            "decision": "REJECT",
            "error": "problem_file_not_found"
        }

    try:
        result = filter_task(
            domain_file,
            problem_file,
            threshold=threshold
        )
    except Exception as exc:
        return {
            "id": task_id,
            "domain_file": domain_file,
            "problem_file": problem_file,
            "decision": "REJECT",
            "error": str(exc)
        }

    decision = (
        "ACCEPT"
        if result["accepted"]
        else "REJECT"
    )

    return {
        "id": task_id,
        "domain_file": domain_file,
        "problem_file": problem_file,
        "decision": decision,
        "report": result["report"]
    }


def build_quality_report(
    input_file=DEFAULT_INPUT_FILE,
    output_file=DEFAULT_OUTPUT_FILE,
    threshold=DEFAULT_THRESHOLD
):
    tasks = load_generated_tasks(input_file)

    results = [
        process_generated_task(
            task,
            threshold=threshold
        )
        for task in tasks
    ]

    accepted = [
        result
        for result in results
        if result["decision"] == "ACCEPT"
    ]

    rejected = [
        result
        for result in results
        if result["decision"] == "REJECT"
    ]

    report = {
        "input_file": input_file,
        "threshold": threshold,
        "total_tasks": len(results),
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "accepted_ids": [
            result["id"]
            for result in accepted
        ],
        "rejected_ids": [
            result["id"]
            for result in rejected
        ],
        "results": results
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    return report


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Run semantic quality verification over "
            "generated AgentGen-style PDDL tasks."
        )
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_FILE
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD
    )

    args = parser.parse_args()

    report = build_quality_report(
        input_file=args.input,
        output_file=args.output,
        threshold=args.threshold
    )

    print()
    print("Quality report created.")
    print("Input:", args.input)
    print("Output:", args.output)
    print("Total tasks:", report["total_tasks"])
    print("Accepted:", report["accepted_count"])
    print("Rejected:", report["rejected_count"])


if __name__ == "__main__":
    main()
