from dataset_loader import load_dataset
from extractor import extract_environment_text

from embedding_retriever import (
    EmbeddingRetriever
)

from multi_query_retriever import (
    MultiQueryRetriever
)

dataset = load_dataset(
    "agentgen_data/merged_gpt_it12.json"
)

for sample in dataset:

    sample["environment_text"] = (
        extract_environment_text(sample)
    )

retriever = EmbeddingRetriever(
    dataset
)

multi_retriever = (
    MultiQueryRetriever(
        retriever
    )
)

results = multi_retriever.retrieve(
    "software build automation"
)

for sample in results:

    print(sample["id"])