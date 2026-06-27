from tarski.io import PDDLReader
from tarski.syntax import Atom


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


def check_trivial_goal(domain_file, problem_file):

    reader = PDDLReader()

    problem = reader.read_problem(
        domain_file,
        problem_file
    )

    goal = problem.goal

    init_facts = list(
        problem.init.as_atoms()
    )

    if isinstance(goal, Atom):
        goal_atoms = [goal]
    else:
        goal_atoms = list(goal.subformulas)

    already_satisfied = True

    for g in goal_atoms:

        if g not in init_facts:
            already_satisfied = False
            break

    return {
        "trivial_problem": already_satisfied
    }
    
def check_undefined_objects(domain_file, problem_file):

    reader = PDDLReader()

    problem = reader.read_problem(
        domain_file,
        problem_file
    )

    goal = problem.goal

    objects = list(
        problem.language.constants()
    )

    defined_objects = set(
        str(obj)
        for obj in objects
    )

    try:
        goal_atoms = list(goal.subformulas)

    except:
        goal_atoms = [goal]

    undefined_objects = []

    for g in goal_atoms:

        for term in g.subterms:

            term_name = str(term)

            if (
                term_name not in defined_objects
                and len(defined_objects) > 0
            ):
                undefined_objects.append(
                    term_name
                )

    return {
        "object_consistency": len(undefined_objects) == 0,
        "undefined_objects": undefined_objects
    }


from tarski.syntax.formulas import (
    Atom,
    CompoundFormula
)


def extract_predicates(formula):

    predicates = set()

    if isinstance(formula, Atom):

        predicates.add(
            str(formula.predicate)
        )

    elif isinstance(
        formula,
        CompoundFormula
    ):

        for sub in formula.subformulas:

            predicates.update(
                extract_predicates(sub)
            )

    return predicates

def check_dead_actions(domain_file, problem_file):

    reader = PDDLReader()

    problem = reader.read_problem(
        domain_file,
        problem_file
    )

    goal = problem.goal

    needed = extract_predicates(
        goal
    )

    useful_actions = set()

    changed = True

    while changed:

        changed = False

        for action_name, action in (
            problem.actions.items()
        ):

            effects = set()

            for eff in action.effects:

                effects.add(
                    str(
                        eff.atom.predicate
                    )
                )

            if effects.intersection(
                needed
            ):

                if action_name not in useful_actions:

                    useful_actions.add(
                        action_name
                    )

                    changed = True

                preconditions = (
                    extract_predicates(
                        action.precondition
                    )
                )

                needed.update(
                    preconditions
                )

    dead_actions = []

    for action_name in (
        problem.actions.keys()
    ):

        if action_name not in useful_actions:

            dead_actions.append(
                action_name
            )

    return {
        "dead_actions": dead_actions,
        "dead_action_count": len(
            dead_actions
        )
    }