(define (domain project_planning)

(:requirements :strips)

(:predicates
    (requirements-written)
    (design-approved)
    (prototype-built)
    (tests-passed)
    (project-delivered)
    (project-impossible-goal-1)
    (project-impossible-goal-2)
    (project-impossible-goal-3)
)

(:action write-requirements
    :parameters ()
    :precondition (and)
    :effect (requirements-written)
)

(:action approve-design
    :parameters ()
    :precondition (requirements-written)
    :effect (design-approved)
)

(:action build-prototype
    :parameters ()
    :precondition (design-approved)
    :effect (prototype-built)
)

(:action run-tests
    :parameters ()
    :precondition (prototype-built)
    :effect (tests-passed)
)

(:action deliver-project
    :parameters ()
    :precondition (tests-passed)
    :effect (project-delivered)
)

)