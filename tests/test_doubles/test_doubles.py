from emush_rag.models.document import Document
from emush_rag.ports.document_reader import DocumentReader


class FakeVectorStore:
    """
    Fake vector store for testing purposes. It stores the documents in memory.
    """

    def __init__(self):
        self.documents = {}
        self.nb_calls = 0

    def get_all(self) -> list[Document]:
        return list(self.documents.values())

    def index_documents(self, documents: list[Document]) -> None:
        for document in documents:
            self.documents[document.metadata["title"]] = document
        self.nb_calls += 1

    def should_be_called_times(self, times: int):
        assert self.nb_calls == times


class InMemoryJsonDocumentReader(DocumentReader):
    json_entries: list[Document]

    def read_documents(self) -> list[Document]:
        return self.json_entries

    def set_json_entries(self, json_entries: list[Document]) -> None:
        self.json_entries = json_entries
