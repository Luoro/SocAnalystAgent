def build_context(results: list[dict]) -> str:

    context_parts = []

    for result in results:

        source = result["metadata"]["source"]

        text = result["text"]

        context_parts.append(
            f"[Source: {source}]\n{text}"
        )

    return "\n\n".join(context_parts)

def build_rag_prompt(
    question: str,
    context: str
) -> str:

    return f"""
You are a cybersecurity assistant.

Answer the user's question using only
the provided context.

If the answer is not present in the context,
say that the information is not available.

Context:

{context}

Question:

{question}
"""
