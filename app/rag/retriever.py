import math


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


class Retriever:

    def __init__(
        self,
        vector_store,
        embedding_model
    ):

        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def search(
        self,
        query: str,
        top_k: int = 3
    ):

        query_embedding = (
            self.embedding_model.embed(query)
        )

        results = []

        for document in self.vector_store.all():

            score = cosine_similarity(
                query_embedding,
                document["embedding"]
            )

            results.append(
                {
                    "score": score,
                    "text": document["text"],
                    "metadata": document["metadata"]
                }
            )

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:top_k]
