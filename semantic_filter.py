import json
import os

from verifier.task_filter import filter_task


def semantic_filter(
    input_file,
    domain_file
):

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:

        dataset = json.load(f)

    accepted = []
    rejected = []

    for item in dataset:

        if "problems" not in item:
            continue

        verified = []

        for i, problem in enumerate(
            item["problems"]
        ):

            temp_problem = (
                f"temp_problem_{i}.pddl"
            )

            with open(
                temp_problem,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(problem)

            try:
                result = filter_task(
                    domain_file,
                    temp_problem
                )
            finally:
                if os.path.exists(temp_problem):
                    os.remove(temp_problem)

            decision = (
                "ACCEPT"
                if result["accepted"]
                else "REJECT"
            )

            verified.append({

                "problem": problem,

                "decision":
                decision,

                "report":
                result["report"]

            })

            if (
                decision
                == "ACCEPT"
            ):

                accepted.append(problem)

            else:

                rejected.append(problem)

        item["verified_problems"] = (
            verified
        )

    return {

        "dataset": dataset,

        "accepted": len(
            accepted
        ),

        "rejected": len(
            rejected
        )

    }
