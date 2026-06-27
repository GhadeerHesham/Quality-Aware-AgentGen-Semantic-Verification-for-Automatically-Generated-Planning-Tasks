(define (domain travel_planning)

(:requirements :strips)

(:predicates
    (passport-ready)
    (flight-booked)
    (hotel-booked)
    (bags-packed)
    (trip-started)
    (travel-impossible-goal-1)
    (travel-impossible-goal-2)
    (travel-impossible-goal-3)
    (travel-unused-1)
    (travel-unused-2)
    (travel-unused-3)
    (travel-unused-4)
    (travel-unused-5)
    (travel-unused-6)
)

(:action prepare-passport
    :parameters ()
    :precondition (and)
    :effect (passport-ready)
)

(:action book-flight
    :parameters ()
    :precondition (passport-ready)
    :effect (flight-booked)
)

(:action book-hotel
    :parameters ()
    :precondition (flight-booked)
    :effect (hotel-booked)
)

(:action pack-bags
    :parameters ()
    :precondition (hotel-booked)
    :effect (bags-packed)
)

(:action start-trip
    :parameters ()
    :precondition (bags-packed)
    :effect (trip-started)
)

(:action travel-unused-action-1
    :parameters ()
    :precondition (and)
    :effect (travel-unused-1)
)

(:action travel-unused-action-2
    :parameters ()
    :precondition (and)
    :effect (travel-unused-2)
)

(:action travel-unused-action-3
    :parameters ()
    :precondition (and)
    :effect (travel-unused-3)
)

(:action travel-unused-action-4
    :parameters ()
    :precondition (and)
    :effect (travel-unused-4)
)

(:action travel-unused-action-5
    :parameters ()
    :precondition (and)
    :effect (travel-unused-5)
)

(:action travel-unused-action-6
    :parameters ()
    :precondition (and)
    :effect (travel-unused-6)
)

)