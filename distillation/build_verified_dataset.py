import argparse
import json
import os
import random


DEFAULT_REPORT_FILE = "generated_tasks_quality_report.json"
DEFAULT_OUTPUT_DIR = "distilled_dataset"
RANDOM_SEED = 42


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def read_text_file(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def save_json(path, data):
    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def quality_label(score, decision):
    if decision == "REJECT":
        return "low"

    if score >= 90:
        return "high"

    if score >= 80:
        return "medium"

    return "low"


def summarize_report(verifier_report):
    dead_action_info = verifier_report["dead_actions"]

    summary = {
        "quality_score": verifier_report["quality_score"],
        "reachable": verifier_report["goal_reachability"]["reachable"],
        "trivial_problem": verifier_report["trivial_goal"]["trivial_problem"],
        "object_consistency": verifier_report["object_consistency"]["object_consistency"],
        "dead_action_count": dead_action_info["dead_action_count"],
        "dead_actions": dead_action_info["dead_actions"]
    }

    return summary


def build_verified_record(result):
    report = result["report"]
    score = report["quality_score"]

    return {
        "id": result["id"],
        "domain_file": result["domain_file"],
        "problem_file": result["problem_file"],
        "domain_pddl": read_text_file(result["domain_file"]),
        "problem_pddl": read_text_file(result["problem_file"]),
        "decision": result["decision"],
        "quality_score": score,
        "quality_label": quality_label(
            score,
            result["decision"]
        ),
        "verifier_report": report,
        "verifier_summary": summarize_report(report)
    }


def build_chat_sample(record):
    prompt = (
        "Evaluate the quality of this generated PDDL planning task. "
        "Return a JSON object with decision, quality_score, quality_label, "
        "and verifier_summary.\n\n"
        "DOMAIN PDDL:\n"
        f"{record['domain_pddl']}\n\n"
        "PROBLEM PDDL:\n"
        f"{record['problem_pddl']}"
    )

    answer = {
        "decision": record["decision"],
        "quality_score": record["quality_score"],
        "quality_label": record["quality_label"],
        "verifier_summary": record["verifier_summary"]
    }

    return {
        "id": record["id"],
        "messages": [
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": json.dumps(
                    answer,
                    indent=2,
                    ensure_ascii=False
                )
            }
        ]
    }


def split_dataset(dataset, train_ratio=0.9):
    shuffled = list(dataset)

    random.seed(RANDOM_SEED)
    random.shuffle(shuffled)

    if len(shuffled) <= 1:
        return shuffled, []

    split_index = max(
        1,
        int(len(shuffled) * train_ratio)
    )

    if split_index >= len(shuffled):
        split_index = len(shuffled) - 1

    return (
        shuffled[:split_index],
        shuffled[split_index:]
    )


def build_verified_dataset(
    report_file=DEFAULT_REPORT_FILE,
    output_dir=DEFAULT_OUTPUT_DIR
):
    report = load_json(report_file)

    records = [
        build_verified_record(result)
        for result in report["results"]
        if "report" in result
    ]

    accepted = [
        record
        for record in records
        if record["decision"] == "ACCEPT"
    ]

    rejected = [
        record
        for record in records
        if record["decision"] == "REJECT"
    ]

    chat_records = [
        build_chat_sample(record)
        for record in records
    ]

    train_chat, valid_chat = split_dataset(
        chat_records
    )

    save_json(
        os.path.join(output_dir, "verified_tasks.json"),
        records
    )
    save_json(
        os.path.join(output_dir, "accepted_verified_tasks.json"),
        accepted
    )
    save_json(
        os.path.join(output_dir, "rejected_verified_tasks.json"),
        rejected
    )
    save_json(
        os.path.join(output_dir, "quality_task_chat.json"),
        chat_records
    )
    save_json(
        os.path.join(output_dir, "quality_task_train_chat.json"),
        train_chat
    )
    save_json(
        os.path.join(output_dir, "quality_task_valid_chat.json"),
        valid_chat
    )

    return {
        "report_file": report_file,
        "output_dir": output_dir,
        "total_records": len(records),
        "accepted_records": len(accepted),
        "rejected_records": len(rejected),
        "chat_records": len(chat_records),
        "train_chat_records": len(train_chat),
        "valid_chat_records": len(valid_chat)
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build quality-aware distillation data from "
            "the generated task verifier report."
        )
    )
    parser.add_argument(
        "--report",
        default=DEFAULT_REPORT_FILE
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR
    )

    args = parser.parse_args()

    summary = build_verified_dataset(
        report_file=args.report,
        output_dir=args.output_dir
    )

    print()
    print("Verified distillation dataset created.")
    print("Report:", summary["report_file"])
    print("Output directory:", summary["output_dir"])
    print("Total records:", summary["total_records"])
    print("Accepted records:", summary["accepted_records"])
    print("Rejected records:", summary["rejected_records"])
    print("Chat records:", summary["chat_records"])
    print("Train chat records:", summary["train_chat_records"])
    print("Valid chat records:", summary["valid_chat_records"])


if __name__ == "__main__":
    main()
