from extractor import extract_environment_text


def search_dataset(dataset, query, top_k=5):

    results = []

    query = query.lower()

    for sample in dataset:

        text = extract_environment_text(
            sample
        ).lower()

        score = text.count(query)

        if score > 0:

            results.append(
                (score, sample)
            )

    results.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return results[:top_k]