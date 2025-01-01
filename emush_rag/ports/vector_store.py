from abc import ABC, abstractmethod

from emush_rag.models.document import Document


class VectorStore(ABC):
    """Vector store interface. This is where we will store our documents for them being used by the RAG model."""

    @abstractmethod
    def index_documents(self, documents: list[Document]) -> None:
        pass

    @abstractmethod
    def get_relevant_documents(self, query: str, max_relevant_documents: int) -> list[Document]:
        pass
