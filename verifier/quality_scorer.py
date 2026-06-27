try:
    from .semantic_verifier import (
        check_goal_reachability,
        check_trivial_goal,
        check_undefined_objects,
        check_dead_actions
    )
except ImportError:
    from semantic_verifier import (
        check_goal_reachability,
        check_trivial_goal,
        check_undefined_objects,
        check_dead_actions
    )


def score_task(domain_file, problem_file):

    score = 100

    reachability = (
        check_goal_reachability(
            domain_file,
            problem_file
        )
    )

    trivial = (
        check_trivial_goal(
            domain_file,
            problem_file
        )
    )

    consistency = (
        check_undefined_objects(
            domain_file,
            problem_file
        )
    )

    dead_actions = (
        check_dead_actions(
            domain_file,
            problem_file
        )
    )

    if not reachability["reachable"]:
        score -= 40

    if trivial["trivial_problem"]:
        score -= 20

    if not consistency["object_consistency"]:
        score -= 20

    score -= (
        dead_actions["dead_action_count"]
        * 5
    )

    score = max(score, 0)

    return {
        "quality_score": score,
        "goal_reachability": reachability,
        "trivial_goal": trivial,
        "object_consistency": consistency,
        "dead_actions": dead_actions
    }
