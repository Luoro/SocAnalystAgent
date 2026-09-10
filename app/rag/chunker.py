def chunk_text(
    text: str,
    chunk_size: int = 100
) -> list[str]:
    """
    Split text into chunks based on words.
    """

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks
