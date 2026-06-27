(define (domain study_planning)

(:requirements :strips)

(:predicates
    (chapter1-studied)
    (chapter2-studied)
    (notes-reviewed)
    (quiz-completed)
    (mock-exam-completed)
    (exam-passed)
    (study-impossible-goal-1)
    (study-impossible-goal-2)
    (study-impossible-goal-3)
    (study-unused-1)
    (study-unused-2)
    (study-unused-3)
    (study-unused-4)
    (study-unused-5)
    (study-unused-6)
)

(:action study-chapter1
    :parameters ()
    :precondition (and)
    :effect (chapter1-studied)
)

(:action study-chapter2
    :parameters ()
    :precondition (chapter1-studied)
    :effect (chapter2-studied)
)

(:action review-notes
    :parameters ()
    :precondition (chapter2-studied)
    :effect (notes-reviewed)
)

(:action take-quiz
    :parameters ()
    :precondition (notes-reviewed)
    :effect (quiz-completed)
)

(:action take-mock-exam
    :parameters ()
    :precondition (quiz-completed)
    :effect (mock-exam-completed)
)

(:action pass-exam
    :parameters ()
    :precondition (mock-exam-completed)
    :effect (exam-passed)
)

(:action study-unused-action-1
    :parameters ()
    :precondition (and)
    :effect (study-unused-1)
)

(:action study-unused-action-2
    :parameters ()
    :precondition (and)
    :effect (study-unused-2)
)

(:action study-unused-action-3
    :parameters ()
    :precondition (and)
    :effect (study-unused-3)
)

(:action study-unused-action-4
    :parameters ()
    :precondition (and)
    :effect (study-unused-4)
)

(:action study-unused-action-5
    :parameters ()
    :precondition (and)
    :effect (study-unused-5)
)

(:action study-unused-action-6
    :parameters ()
    :precondition (and)
    :effect (study-unused-6)
)

)