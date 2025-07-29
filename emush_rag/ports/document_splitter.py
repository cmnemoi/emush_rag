from abc import ABC, abstractmethod

from emush_rag.models.document import Document


class DocumentSplitter(ABC):
    @abstractmethod
    def split(self, document: Document) -> list[Document]:
        pass
