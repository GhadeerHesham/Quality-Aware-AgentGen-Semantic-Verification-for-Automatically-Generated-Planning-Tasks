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

)