from abc import ABC, abstractmethod


class EmbeddingModel(ABC):

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass


class MockEmbeddingModel(EmbeddingModel):

    def embed(self, text: str) -> list[float]:
        """
        Temporary embedding implementation.

        This is only for testing the RAG architecture.
        It is NOT a semantic embedding model.
        """

        values = []

        for character in text[:32]:

            values.append(
                ord(character) / 1000
            )

        while len(values) < 32:
            values.append(0.0)

        return values
