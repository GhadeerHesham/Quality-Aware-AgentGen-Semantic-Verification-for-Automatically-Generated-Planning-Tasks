from semantic_filter import semantic_filter

result = semantic_filter(

    "agentgen_data/merged_gpt_it12.json",

    "domains/study_domain.pddl"

)

print()

print("Accepted:")

print(result["accepted"])

print()

print("Rejected:")

print(result["rejected"])