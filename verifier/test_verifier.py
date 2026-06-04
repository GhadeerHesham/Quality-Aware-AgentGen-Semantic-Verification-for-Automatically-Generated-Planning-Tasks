from verifier import verify_plan

sample_plan = """
study-chapter1
study-chapter2
review-notes
take-quiz
take-mock-exam
pass-exam
"""

print(verify_plan(sample_plan))