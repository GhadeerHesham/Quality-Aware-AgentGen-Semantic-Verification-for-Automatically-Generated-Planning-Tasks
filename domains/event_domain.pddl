(define (domain event_planning)

(:requirements :strips)

(:predicates
    (venue-booked)
    (catering-arranged)
    (event-ready)
)

(:action book-venue
    :parameters ()
    :precondition (and)
    :effect (venue-booked)
)

(:action arrange-catering
    :parameters ()
    :precondition (venue-booked)
    :effect (catering-arranged)
)

(:action prepare-event
    :parameters ()
    :precondition (catering-arranged)
    :effect (event-ready)
)

)
