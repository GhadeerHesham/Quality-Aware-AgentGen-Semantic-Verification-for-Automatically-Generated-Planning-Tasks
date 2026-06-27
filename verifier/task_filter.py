try:
    from .quality_scorer import score_task
except ImportError:
    from quality_scorer import score_task


def filter_task(
    domain_file,
    problem_file,
    threshold=80
):

    report = score_task(
        domain_file,
        problem_file
    )

    accepted = (
        report["quality_score"]
        >= threshold
    )

    return {
        "accepted": accepted,
        "report": report
    }
