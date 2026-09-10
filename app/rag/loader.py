from pathlib import Path


def load_documents(directory: str) -> list[dict]:
    """
    Load Markdown documents from a directory.
    """

    documents = []

    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge directory not found: {directory}"
        )

    for file in path.glob("*.md"):

        content = file.read_text(
            encoding="utf-8"
        )

        documents.append(
            {
                "source": file.name,
                "content": content
            }
        )

    return documents
