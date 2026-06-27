from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

class EmbeddingRetriever:

    def __init__(self, dataset):

        self.dataset = dataset

        texts = [
            sample["environment_text"]
            for sample in dataset
        ]

        self.embeddings = model.encode(
            texts,
            convert_to_numpy=True
        )

    def retrieve(self, query, top_k=5):

        query_embedding = model.encode(
            query,
            convert_to_numpy=True
        )

        scores = np.dot(
            self.embeddings,
            query_embedding
        )

        ranked = np.argsort(scores)[::-1]

        return [
            self.dataset[i]
            for i in ranked[:top_k]
        ]