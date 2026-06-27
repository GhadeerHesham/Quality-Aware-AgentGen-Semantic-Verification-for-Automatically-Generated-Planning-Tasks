from quality_scorer import score_task

result = score_task(
    "domains/study_domain.pddl",
    "problems/study_easy.pddl"
)

print(result)