from dataset_loader import load_dataset
from retriever import search_dataset

dataset = load_dataset(
    "agentgen_data/merged_gpt_it12.json"
)

results = search_dataset(
    dataset,
    "software"
)

print("Results Found:")
print(len(results))

for score, sample in results:

    print("\nID:", sample["id"])
    print("Score:", score)