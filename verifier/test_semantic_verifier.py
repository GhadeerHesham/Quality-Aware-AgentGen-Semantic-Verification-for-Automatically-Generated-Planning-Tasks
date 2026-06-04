from semantic_verifier import check_goal_reachability

result = check_goal_reachability(
    "domains/study_domain.pddl",
    "problems/study_easy.pddl"
)

print(result)