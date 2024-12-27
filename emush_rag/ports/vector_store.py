from typing import Protocol

from emush_rag.models.document import Document


class VectorStore(Protocol):
    """Vector store interface. This is where we will store our documents for them being used by the RAG model."""

    def index_documents(self, documents: list[Document]) -> None: ...
