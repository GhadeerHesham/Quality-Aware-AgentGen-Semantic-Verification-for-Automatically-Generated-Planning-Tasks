import argparse
import json
import os


DOMAINS = [
    {
        "name": "study",
        "domain": "study_planning",
        "predicates": [
            "chapter1-studied",
            "chapter2-studied",
            "notes-reviewed",
            "quiz-completed",
            "mock-exam-completed",
            "exam-passed"
        ],
        "actions": [
            "study-chapter1",
            "study-chapter2",
            "review-notes",
            "take-quiz",
            "take-mock-exam",
            "pass-exam"
        ]
    },
    {
        "name": "event",
        "domain": "event_planning",
        "predicates": [
            "venue-booked",
            "catering-arranged",
            "speaker-confirmed",
            "guests-invited",
            "event-ready"
        ],
        "actions": [
            "book-venue",
            "arrange-catering",
            "confirm-speaker",
            "invite-guests",
            "prepare-event"
        ]
    },
    {
        "name": "travel",
        "domain": "travel_planning",
        "predicates": [
            "passport-ready",
            "flight-booked",
            "hotel-booked",
            "bags-packed",
            "trip-started"
        ],
        "actions": [
            "prepare-passport",
            "book-flight",
            "book-hotel",
            "pack-bags",
            "start-trip"
        ]
    },
    {
        "name": "cooking",
        "domain": "cooking_planning",
        "predicates": [
            "ingredients-ready",
            "vegetables-chopped",
            "sauce-cooked",
            "meal-plated",
            "dinner-served"
        ],
        "actions": [
            "prepare-ingredients",
            "chop-vegetables",
            "cook-sauce",
            "plate-meal",
            "serve-dinner"
        ]
    },
    {
        "name": "project",
        "domain": "project_planning",
        "predicates": [
            "requirements-written",
            "design-approved",
            "prototype-built",
            "tests-passed",
            "project-delivered"
        ],
        "actions": [
            "write-requirements",
            "approve-design",
            "build-prototype",
            "run-tests",
            "deliver-project"
        ]
    },
    {
        "name": "shopping",
        "domain": "shopping_planning",
        "predicates": [
            "list-made",
            "store-visited",
            "items-bought",
            "payment-complete",
            "shopping-done"
        ],
        "actions": [
            "make-list",
            "visit-store",
            "buy-items",
            "complete-payment",
            "finish-shopping"
        ]
    }
]


def ensure_dir(path):
    os.makedirs(
        path,
        exist_ok=True
    )


def action_block(action_name, effect, precondition=None):
    precondition_text = (
        "(and)"
        if precondition is None
        else f"({precondition})"
    )

    return (
        f"(:action {action_name}\n"
        "    :parameters ()\n"
        f"    :precondition {precondition_text}\n"
        f"    :effect ({effect})\n"
        ")\n"
    )


def render_domain(spec, extra_dead_actions=0):
    predicates = list(spec["predicates"])
    for index in range(3):
        predicates.append(
            f"{spec['name']}-impossible-goal-{index + 1}"
        )

    for index in range(extra_dead_actions):
        predicates.append(
            f"{spec['name']}-unused-{index + 1}"
        )

    predicate_text = "\n".join(
        f"    ({predicate})"
        for predicate in predicates
    )

    action_text = []

    for index, action_name in enumerate(spec["actions"]):
        precondition = (
            None
            if index == 0
            else spec["predicates"][index - 1]
        )
        action_text.append(
            action_block(
                action_name,
                spec["predicates"][index],
                precondition
            )
        )

    for index in range(extra_dead_actions):
        action_text.append(
            action_block(
                f"{spec['name']}-unused-action-{index + 1}",
                f"{spec['name']}-unused-{index + 1}",
                None
            )
        )

    return (
        f"(define (domain {spec['domain']})\n\n"
        "(:requirements :strips)\n\n"
        "(:predicates\n"
        f"{predicate_text}\n"
        ")\n\n"
        + "\n".join(action_text)
        + "\n)"
    )


def render_problem(problem_name, domain_name, goal, init=None):
    init = init or []
    init_text = " ".join(
        f"({fact})"
        for fact in init
    )

    return (
        f"(define (problem {problem_name})\n"
        f" (:domain {domain_name})\n\n"
        f" (:init {init_text})\n\n"
        " (:goal\n"
        f"    ({goal})\n"
        " )\n"
        ")"
    )


def write_text(path, text):
    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text)


def build_benchmark(
    domains_dir="benchmark_domains",
    problems_dir="benchmark_problems",
    output_file="generated_tasks.json"
):
    ensure_dir(domains_dir)
    ensure_dir(problems_dir)

    tasks = []

    for spec in DOMAINS:
        base_domain_file = os.path.join(
            domains_dir,
            f"{spec['name']}_domain.pddl"
        )
        dead_domain_file = os.path.join(
            domains_dir,
            f"{spec['name']}_dead_branch_domain.pddl"
        )

        write_text(
            base_domain_file,
            render_domain(spec)
        )
        write_text(
            dead_domain_file,
            render_domain(
                spec,
                extra_dead_actions=6
            )
        )

        for index, predicate in enumerate(spec["predicates"]):
            task_id = (
                f"{spec['name']}_chain_goal_{index + 1}"
            )
            problem_file = os.path.join(
                problems_dir,
                f"{task_id}.pddl"
            )
            write_text(
                problem_file,
                render_problem(
                    task_id,
                    spec["domain"],
                    predicate
                )
            )
            tasks.append({
                "id": task_id,
                "domain_file": base_domain_file,
                "problem_file": problem_file,
                "category": "chain_goal"
            })

        final_goal = spec["predicates"][-1]

        cases = [
            (
                "trivial_final_goal",
                base_domain_file,
                final_goal,
                [final_goal],
                "trivial_goal"
            ),
            (
                "dead_branch_final_goal",
                dead_domain_file,
                final_goal,
                [],
                "dead_actions"
            ),
            (
                "trivial_dead_branch_goal",
                dead_domain_file,
                final_goal,
                [final_goal],
                "combined_quality_failure"
            )
        ]

        for index in range(3):
            cases.append(
                (
                    f"unreachable_goal_{index + 1}",
                    base_domain_file,
                    f"{spec['name']}-impossible-goal-{index + 1}",
                    [],
                    "unreachable_goal"
                )
            )

        for suffix, domain_file, goal, init, category in cases:
            task_id = f"{spec['name']}_{suffix}"
            problem_file = os.path.join(
                problems_dir,
                f"{task_id}.pddl"
            )
            write_text(
                problem_file,
                render_problem(
                    task_id,
                    spec["domain"],
                    goal,
                    init=init
                )
            )
            tasks.append({
                "id": task_id,
                "domain_file": domain_file,
                "problem_file": problem_file,
                "category": category
            })

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            tasks,
            f,
            indent=4
        )

    return tasks


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a reproducible benchmark suite of "
            "AgentGen-style PDDL tasks for quality verification."
        )
    )
    parser.add_argument(
        "--domains-dir",
        default="benchmark_domains"
    )
    parser.add_argument(
        "--problems-dir",
        default="benchmark_problems"
    )
    parser.add_argument(
        "--output",
        default="generated_tasks.json"
    )

    args = parser.parse_args()
    tasks = build_benchmark(
        domains_dir=args.domains_dir,
        problems_dir=args.problems_dir,
        output_file=args.output
    )

    print()
    print("Benchmark tasks generated.")
    print("Output:", args.output)
    print("Tasks:", len(tasks))
    print("Domains directory:", args.domains_dir)
    print("Problems directory:", args.problems_dir)


if __name__ == "__main__":
    main()
