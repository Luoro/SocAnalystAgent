from .loader import load_documents
from .chunker import chunk_text
from .embeddings import MockEmbeddingModel
from .vector_store import InMemoryVectorStore
from .retriever import Retriever


def build_knowledge_base(
    directory: str
):

    documents = load_documents(directory)

    embedding_model = MockEmbeddingModel()

    vector_store = InMemoryVectorStore()

    for document in documents:

        chunks = chunk_text(
            document["content"]
        )

        for chunk in chunks:

            embedding = embedding_model.embed(
                chunk
            )

            vector_store.add(
                text=chunk,
                embedding=embedding,
                metadata={
                    "source": document["source"]
                }
            )

    return vector_store, embedding_model
