(define (domain shopping_planning)

(:requirements :strips)

(:predicates
    (list-made)
    (store-visited)
    (items-bought)
    (payment-complete)
    (shopping-done)
    (shopping-impossible-goal-1)
    (shopping-impossible-goal-2)
    (shopping-impossible-goal-3)
    (shopping-unused-1)
    (shopping-unused-2)
    (shopping-unused-3)
    (shopping-unused-4)
    (shopping-unused-5)
    (shopping-unused-6)
)

(:action make-list
    :parameters ()
    :precondition (and)
    :effect (list-made)
)

(:action visit-store
    :parameters ()
    :precondition (list-made)
    :effect (store-visited)
)

(:action buy-items
    :parameters ()
    :precondition (store-visited)
    :effect (items-bought)
)

(:action complete-payment
    :parameters ()
    :precondition (items-bought)
    :effect (payment-complete)
)

(:action finish-shopping
    :parameters ()
    :precondition (payment-complete)
    :effect (shopping-done)
)

(:action shopping-unused-action-1
    :parameters ()
    :precondition (and)
    :effect (shopping-unused-1)
)

(:action shopping-unused-action-2
    :parameters ()
    :precondition (and)
    :effect (shopping-unused-2)
)

(:action shopping-unused-action-3
    :parameters ()
    :precondition (and)
    :effect (shopping-unused-3)
)

(:action shopping-unused-action-4
    :parameters ()
    :precondition (and)
    :effect (shopping-unused-4)
)

(:action shopping-unused-action-5
    :parameters ()
    :precondition (and)
    :effect (shopping-unused-5)
)

(:action shopping-unused-action-6
    :parameters ()
    :precondition (and)
    :effect (shopping-unused-6)
)

)