import json
import os
from collections import Counter, defaultdict


QUALITY_REPORT_FILE = "generated_tasks_quality_report.json"
MODEL_EVALUATION_FILE = "distilled_model/student_evaluation.json"
OUTPUT_FILE = "results/thesis_comparison_summary.json"


def load_json(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


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


def task_family(task_id):
    return task_id.split(
        "_",
        1
    )[0]


def task_category(task_id):
    if "unreachable" in task_id:
        return "unreachable_goal"
    if "trivial" in task_id:
        return "trivial_goal"
    if "dead_branch" in task_id:
        return "dead_branch"
    if "combined_quality_failure" in task_id:
        return "combined_quality_failure"
    if "trivial_dead_branch" in task_id:
        return "combined_quality_failure"
    if "chain_goal" in task_id:
        return "chain_goal"
    return "other"


def collect_failure_flags(result):
    report = result.get(
        "report",
        {}
    )
    flags = []

    if not report.get(
        "goal_reachability",
        {}
    ).get(
        "reachable",
        True
    ):
        flags.append("unreachable_goal")

    if report.get(
        "trivial_goal",
        {}
    ).get(
        "trivial_problem",
        False
    ):
        flags.append("trivial_goal")

    if not report.get(
        "object_consistency",
        {}
    ).get(
        "object_consistency",
        True
    ):
        flags.append("object_consistency")

    if report.get(
        "dead_actions",
        {}
    ).get(
        "dead_action_count",
        0
    ):
        flags.append("dead_actions")

    return flags


def build_summary(
    report_file=QUALITY_REPORT_FILE,
    model_evaluation_file=MODEL_EVALUATION_FILE,
    output_file=OUTPUT_FILE
):
    report = load_json(report_file)
    model_evaluation = load_json(model_evaluation_file)
    results = report["results"]

    decision_counts = Counter(
        result["decision"]
        for result in results
    )
    family_counts = defaultdict(Counter)
    category_counts = defaultdict(Counter)
    failure_counts = Counter()
    score_by_category = defaultdict(list)

    for result in results:
        decision = result["decision"]
        family_counts[task_family(result["id"])][decision] += 1
        category_counts[task_category(result["id"])][decision] += 1

        report_payload = result.get(
            "report",
            {}
        )
        if "quality_score" in report_payload:
            score_by_category[task_category(result["id"])].append(
                report_payload["quality_score"]
            )

        for flag in collect_failure_flags(result):
            failure_counts[flag] += 1

    category_summary = {}

    for category, scores in score_by_category.items():
        category_summary[category] = {
            "count": len(scores),
            "average_quality_score": round(
                sum(scores) / len(scores),
                2
            ),
            "decisions": dict(
                category_counts[category]
            )
        }

    summary = {
        "benchmark": {
            "source": report["input_file"],
            "total_tasks": report["total_tasks"],
            "acceptance_threshold": report["threshold"],
            "families": {
                family: dict(counts)
                for family, counts in family_counts.items()
            },
            "categories": category_summary
        },
        "original_agentgen_style_baseline": {
            "description": (
                "Baseline assumes generated tasks are passed forward "
                "without the quality-aware verifier filter."
            ),
            "tasks_passed_forward": report["total_tasks"],
            "semantic_quality_failures_not_filtered": report["rejected_count"]
        },
        "quality_aware_pipeline": {
            "accepted_tasks": decision_counts.get(
                "ACCEPT",
                0
            ),
            "rejected_tasks": decision_counts.get(
                "REJECT",
                0
            ),
            "rejection_rate": round(
                decision_counts.get(
                    "REJECT",
                    0
                ) / report["total_tasks"],
                4
            ),
            "failure_flags": dict(failure_counts)
        },
        "student_model": {
            "evaluation_method": model_evaluation.get(
                "evaluation_method"
            ),
            "total_examples": model_evaluation.get(
                "total_examples"
            ),
            "leave_one_out_accuracy": model_evaluation.get(
                "accuracy"
            ),
            "fitted_model_accuracy": model_evaluation.get(
                "fitted_model_accuracy"
            )
        }
    }

    save_json(
        output_file,
        summary
    )

    return summary


def main():
    summary = build_summary()

    print()
    print("Thesis comparison summary created.")
    print("Output:", OUTPUT_FILE)
    print("Benchmark tasks:", summary["benchmark"]["total_tasks"])
    print(
        "Quality-aware accepted:",
        summary["quality_aware_pipeline"]["accepted_tasks"]
    )
    print(
        "Quality-aware rejected:",
        summary["quality_aware_pipeline"]["rejected_tasks"]
    )
    print(
        "Student leave-one-out accuracy:",
        summary["student_model"]["leave_one_out_accuracy"]
    )


if __name__ == "__main__":
    main()
