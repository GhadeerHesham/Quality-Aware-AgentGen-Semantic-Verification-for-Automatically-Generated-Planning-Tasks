(define (domain event_planning)

(:requirements :strips)

(:predicates
    (venue-booked)
    (catering-arranged)
    (speaker-confirmed)
    (guests-invited)
    (event-ready)
    (event-impossible-goal-1)
    (event-impossible-goal-2)
    (event-impossible-goal-3)
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

(:action confirm-speaker
    :parameters ()
    :precondition (catering-arranged)
    :effect (speaker-confirmed)
)

(:action invite-guests
    :parameters ()
    :precondition (speaker-confirmed)
    :effect (guests-invited)
)

(:action prepare-event
    :parameters ()
    :precondition (guests-invited)
    :effect (event-ready)
)

)