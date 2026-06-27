class MultiQueryRetriever:

    def __init__(self, retriever):

        self.retriever = retriever

    def generate_queries(self, user_query):

        return [
            user_query,
            user_query + " planning",
            user_query + " automation",
            user_query + " workflow"
        ]

    def retrieve(self, user_query, top_k=5):

        queries = self.generate_queries(
            user_query
        )

        unique_results = {}

        for q in queries:

            results = self.retriever.retrieve(
                q,
                top_k=top_k
            )

            for sample in results:

                unique_results[
                    sample["id"]
                ] = sample

        return list(
            unique_results.values()
        )[:top_k]