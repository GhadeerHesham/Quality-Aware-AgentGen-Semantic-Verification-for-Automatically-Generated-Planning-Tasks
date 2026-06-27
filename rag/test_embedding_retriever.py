from dataset_loader import load_dataset
from extractor import extract_environment_text
from embedding_retriever import EmbeddingRetriever

# Load AgentGen dataset
dataset = load_dataset(
    "agentgen_data/merged_gpt_it12.json"
)

# Add environment text to each sample
for sample in dataset:
    sample["environment_text"] = (
        extract_environment_text(sample)
    )

print("Dataset loaded:", len(dataset))

# Build retriever
retriever = EmbeddingRetriever(dataset)

query = """
software build automation
makefile modification
testing build process
documentation
"""

print("\nSearching...\n")

results = retriever.retrieve(
    query,
    top_k=5
)

for i, sample in enumerate(results, start=1):

    print(f"Result {i}")
    print("ID:", sample["id"])
    print("-" * 50)