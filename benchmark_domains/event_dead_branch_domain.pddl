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
    (event-unused-1)
    (event-unused-2)
    (event-unused-3)
    (event-unused-4)
    (event-unused-5)
    (event-unused-6)
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

(:action event-unused-action-1
    :parameters ()
    :precondition (and)
    :effect (event-unused-1)
)

(:action event-unused-action-2
    :parameters ()
    :precondition (and)
    :effect (event-unused-2)
)

(:action event-unused-action-3
    :parameters ()
    :precondition (and)
    :effect (event-unused-3)
)

(:action event-unused-action-4
    :parameters ()
    :precondition (and)
    :effect (event-unused-4)
)

(:action event-unused-action-5
    :parameters ()
    :precondition (and)
    :effect (event-unused-5)
)

(:action event-unused-action-6
    :parameters ()
    :precondition (and)
    :effect (event-unused-6)
)

)