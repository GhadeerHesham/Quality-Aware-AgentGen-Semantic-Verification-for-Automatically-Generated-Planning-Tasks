from tarski.io import PDDLReader

reader = PDDLReader()

problem = reader.read_problem(
    "domains/study_domain.pddl",
    "problems/study_easy.pddl"
)

print("GOAL:")
print(problem.goal)

print("\nGOAL TYPE:")
print(type(problem.goal))