from tarski.io import PDDLReader


def check_goal_reachability(domain_file, problem_file):

    reader = PDDLReader()

    problem = reader.read_problem(
        domain_file,
        problem_file
    )

    goal = problem.goal

    effect_predicates = set()

    for action in problem.actions.values():

        for eff in action.effects:

            effect_predicates.add(
                str(eff.atom.predicate)
            )

    unreachable_goals = []

    try:
        goal_atoms = list(goal.subformulas)

    except:
        goal_atoms = [goal]

    for g in goal_atoms:

        predicate_name = str(g.predicate)

        if predicate_name not in effect_predicates:

            unreachable_goals.append(
                predicate_name
            )

    return {
        "reachable": len(unreachable_goals) == 0,
        "unreachable_goals": unreachable_goals
    }