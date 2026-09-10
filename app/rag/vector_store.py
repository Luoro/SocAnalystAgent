class InMemoryVectorStore:

    def __init__(self):
        self.documents = []

    def add(
        self,
        text: str,
        embedding: list[float],
        metadata: dict
    ):

        self.documents.append(
            {
                "text": text,
                "embedding": embedding,
                "metadata": metadata
            }
        )

    def all(self):
        return self.documents
