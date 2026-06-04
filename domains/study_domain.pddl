(define (domain study_planning)

(:requirements :strips)

(:predicates
    (chapter1-studied)
    (chapter2-studied)
    (notes-reviewed)
    (quiz-completed)
    (mock-exam-completed)
    (exam-passed)
)

(:action study-chapter1
    :precondition (and)
    :effect (chapter1-studied)
)

(:action study-chapter2
    :precondition (chapter1-studied)
    :effect (chapter2-studied)
)

(:action review-notes
    :precondition (and
        (chapter1-studied)
        (chapter2-studied)
    )
    :effect (notes-reviewed)
)

(:action take-quiz
    :precondition (notes-reviewed)
    :effect (quiz-completed)
)

(:action take-mock-exam
    :precondition (quiz-completed)
    :effect (mock-exam-completed)
)

(:action pass-exam
    :precondition (mock-exam-completed)
    :effect (exam-passed)
)

)