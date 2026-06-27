from task_filter import filter_task

result = filter_task(
    "domains/study_domain.pddl",
    "problems/study_easy.pddl"
)

print(result)