import json
import os
import sys

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        ".."
    )
)

sys.path.append(project_root)

from verifier.quality_scorer import score_task


INPUT_FILE = "generated_tasks.json"
OUTPUT_FILE = "verified_tasks.json"


def semantic_verification():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        dataset = json.load(f)

    verified_dataset = []

    accepted = 0
    rejected = 0

    for index, item in enumerate(dataset):

        print(
            f"Verifying Task {index + 1}"
        )

        domain_file = item["domain_file"]
        problem_file = item["problem_file"]

        report = score_task(
            domain_file,
            problem_file
        )

        if report["quality_score"] >= 80:

            decision = "ACCEPT"
            accepted += 1

        else:

            decision = "REJECT"
            rejected += 1

        item["quality_score"] = (
            report["quality_score"]
        )

        item["decision"] = decision

        item["verification_report"] = report

        verified_dataset.append(item)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            verified_dataset,
            f,
            indent=4
        )

    print()

    print("Verification Complete")

    print("Accepted:", accepted)

    print("Rejected:", rejected)


if __name__ == "__main__":

    semantic_verification()