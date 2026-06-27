(define (domain cooking_planning)

(:requirements :strips)

(:predicates
    (ingredients-ready)
    (vegetables-chopped)
    (sauce-cooked)
    (meal-plated)
    (dinner-served)
    (cooking-impossible-goal-1)
    (cooking-impossible-goal-2)
    (cooking-impossible-goal-3)
    (cooking-unused-1)
    (cooking-unused-2)
    (cooking-unused-3)
    (cooking-unused-4)
    (cooking-unused-5)
    (cooking-unused-6)
)

(:action prepare-ingredients
    :parameters ()
    :precondition (and)
    :effect (ingredients-ready)
)

(:action chop-vegetables
    :parameters ()
    :precondition (ingredients-ready)
    :effect (vegetables-chopped)
)

(:action cook-sauce
    :parameters ()
    :precondition (vegetables-chopped)
    :effect (sauce-cooked)
)

(:action plate-meal
    :parameters ()
    :precondition (sauce-cooked)
    :effect (meal-plated)
)

(:action serve-dinner
    :parameters ()
    :precondition (meal-plated)
    :effect (dinner-served)
)

(:action cooking-unused-action-1
    :parameters ()
    :precondition (and)
    :effect (cooking-unused-1)
)

(:action cooking-unused-action-2
    :parameters ()
    :precondition (and)
    :effect (cooking-unused-2)
)

(:action cooking-unused-action-3
    :parameters ()
    :precondition (and)
    :effect (cooking-unused-3)
)

(:action cooking-unused-action-4
    :parameters ()
    :precondition (and)
    :effect (cooking-unused-4)
)

(:action cooking-unused-action-5
    :parameters ()
    :precondition (and)
    :effect (cooking-unused-5)
)

(:action cooking-unused-action-6
    :parameters ()
    :precondition (and)
    :effect (cooking-unused-6)
)

)