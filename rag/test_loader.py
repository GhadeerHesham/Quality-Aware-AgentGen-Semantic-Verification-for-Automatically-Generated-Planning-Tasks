from dataset_loader import (
    load_dataset,
    get_sample
)

dataset = load_dataset(
    "agentgen_data/merged_gpt_it12.json"
)

print("Total Samples:")
print(len(dataset))

sample = get_sample(dataset)

print("\nSample ID:")
print(sample["id"])

print("\nTask:")
print(sample["task"])

print("\nConversation Count:")
print(len(sample["conversations"]))

print("\nFirst Conversation:")
print(sample["conversations"][0])