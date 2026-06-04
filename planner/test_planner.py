from planner import run_planner

output = run_planner(
    "domains/study_domain.pddl",
    "problems/study_hard.pddl"
)

print(output)