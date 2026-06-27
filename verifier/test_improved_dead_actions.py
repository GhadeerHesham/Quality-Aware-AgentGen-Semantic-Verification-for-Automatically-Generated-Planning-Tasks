from improved_dead_action_verifier import (
    check_dead_actions_improved
)

result = (
    check_dead_actions_improved(
        "domains/study_domain.pddl",
        "problems/study_full_goal.pddl"
    )
)

print(result)