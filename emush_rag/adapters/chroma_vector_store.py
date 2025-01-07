from typing import Dict, Union, cast

from chromadb.api import ClientAPI
from chromadb.api.types import EmbeddingFunction, QueryResult
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from emush_rag.config import Config
from emush_rag.models.document import Document, DocumentMetadata
from emush_rag.ports.vector_store import VectorStore

ChromaMetadata = Dict[str, Union[str, int, float, bool]]

config = Config()


class ChromaVectorStore(VectorStore):
    def __init__(
        self,
        client: ClientAPI,
        collection_name: str,
        embedding_function: EmbeddingFunction | None = DefaultEmbeddingFunction(),
    ):
        self.client = client
        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=embedding_function
        )

    def index_documents(self, documents: list[Document]) -> None:
        if not documents:
            return

        self.collection.add(
            documents=[doc.content for doc in documents],
            metadatas=[cast(ChromaMetadata, doc.metadata) for doc in documents],
            ids=[document.generate_id() for document in documents],
        )

    def get_relevant_documents(self, query: str, max_relevant_documents: int) -> list[Document]:
        query_results = self._query_collection(query, max_relevant_documents)
        if not self._has_valid_results(query_results):
            return []
        return self._create_documents_from_results(query_results)

    def get_all_documents(self) -> list[Document]:
        results = self.collection.get()
        if not results["documents"] or not results["metadatas"]:
            return []

        return [
            Document(
                content=content,
                metadata=cast(DocumentMetadata, metadata),
            )
            for content, metadata in zip(results["documents"], results["metadatas"])
        ]

    def _query_collection(self, query: str, max_relevant_documents: int) -> QueryResult:
        return self.collection.query(
            query_texts=[query],
            n_results=max_relevant_documents,
        )

    def _has_valid_results(self, results: QueryResult) -> bool:
        return bool(
            results["documents"]
            and results["metadatas"]
            and len(results["documents"]) > 0
            and len(results["metadatas"]) > 0
        )

    def _create_documents_from_results(self, results: QueryResult) -> list[Document]:
        if not self._has_valid_results(results):
            return []

        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        return [
            self._create_document(content, cast(ChromaMetadata, metadata))
            for content, metadata in zip(documents, metadatas)
        ]

    def _create_document(self, content: str, metadata: ChromaMetadata) -> Document:
        return Document(
            content=content,
            metadata=cast(DocumentMetadata, metadata),
        )
