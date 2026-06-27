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

)