from abc import ABC, abstractmethod

from emush_rag.models.document import Document


class DocumentReader(ABC):
    """Port interface for reading documents from a source"""

    @abstractmethod
    def read_documents(self) -> list[Document]:
        """Read documents from a source and return them as a list of Documents"""
        pass
