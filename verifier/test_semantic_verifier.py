from semantic_verifier import (
    check_goal_reachability,
    check_trivial_goal,
    check_undefined_objects,
    check_dead_actions
)

print(
    check_goal_reachability(
        "domains/study_domain.pddl",
        "problems/study_easy.pddl"
    )
)

print(
    check_trivial_goal(
        "domains/study_domain.pddl",
        "problems/study_easy.pddl"
    )
)

print(
    check_undefined_objects(
        "domains/study_domain.pddl",
        "problems/study_easy.pddl"
    )
)

print(
    check_dead_actions(
        "domains/study_domain.pddl",
        "problems/study_easy.pddl"
    )
)