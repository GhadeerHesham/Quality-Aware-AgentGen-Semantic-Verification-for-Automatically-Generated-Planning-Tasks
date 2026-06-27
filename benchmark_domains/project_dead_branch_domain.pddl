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
    (project-unused-1)
    (project-unused-2)
    (project-unused-3)
    (project-unused-4)
    (project-unused-5)
    (project-unused-6)
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

(:action project-unused-action-1
    :parameters ()
    :precondition (and)
    :effect (project-unused-1)
)

(:action project-unused-action-2
    :parameters ()
    :precondition (and)
    :effect (project-unused-2)
)

(:action project-unused-action-3
    :parameters ()
    :precondition (and)
    :effect (project-unused-3)
)

(:action project-unused-action-4
    :parameters ()
    :precondition (and)
    :effect (project-unused-4)
)

(:action project-unused-action-5
    :parameters ()
    :precondition (and)
    :effect (project-unused-5)
)

(:action project-unused-action-6
    :parameters ()
    :precondition (and)
    :effect (project-unused-6)
)

)