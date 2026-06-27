from tarski.io import PDDLReader

reader = PDDLReader()

problem = reader.read_problem(
    "domains/study_domain.pddl",
    "problems/study_easy.pddl"
)

for action_name, action in problem.actions.items():

    print("\n====================")
    print("ACTION:", action_name)

    print("PRECONDITION:")
    print(action.precondition)

    print("TYPE:")
    print(type(action.precondition))

    print("EFFECTS:")

    for eff in action.effects:
        print(eff)