from typing import List

from emush_rag.models.document import Document
from emush_rag.ports.document_reader import DocumentReader
from emush_rag.ports.llm_client import ChatMessage, LLMClient
from emush_rag.ports.vector_store import VectorStore


class FakeVectorStore(VectorStore):
    """
    Fake vector store for testing purposes. It returns predefined documents.
    """

    def __init__(self, documents_to_return: List[Document] | None = None):
        self.documents_to_return = documents_to_return or []
        self.indexed_documents: List[Document] = []
        self.nb_calls = 0

    def get_all(self) -> List[Document]:
        return self.indexed_documents

    def index_documents(self, documents: List[Document]) -> None:
        self.indexed_documents.extend(documents)
        self.nb_calls += 1

    def get_relevant_documents(self, query: str) -> List[Document]:
        return self.documents_to_return

    def should_be_called_times(self, times: int):
        assert self.nb_calls == times


class FakeLLMClient(LLMClient):
    """
    Fake LLM client for testing purposes. It returns predefined responses.
    """

    def __init__(
        self, expected_response: str = "This is a fake response", expected_messages: List[ChatMessage] | None = None
    ):
        self.expected_response = expected_response
        self.expected_messages = expected_messages

    def complete(self, messages: List[ChatMessage]) -> str:
        if self.expected_messages is not None:
            assert messages == self.expected_messages
        return self.expected_response


class InMemoryJsonDocumentReader(DocumentReader):
    """
    Fake document reader for testing purposes. It returns predefined documents.
    """

    json_entries: List[Document]

    def read_documents(self) -> List[Document]:
        return self.json_entries

    def set_json_entries(self, json_entries: List[Document]) -> None:
        self.json_entries = json_entries
