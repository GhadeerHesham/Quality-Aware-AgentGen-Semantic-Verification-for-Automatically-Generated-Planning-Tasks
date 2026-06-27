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

)