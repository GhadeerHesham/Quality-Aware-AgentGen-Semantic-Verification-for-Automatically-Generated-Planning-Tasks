from tarski.io import PDDLReader
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


def check_dead_actions_improved(
    domain_file,
    problem_file
):

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
