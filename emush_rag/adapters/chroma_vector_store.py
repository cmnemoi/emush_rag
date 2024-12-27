from typing import Dict, Union, cast

import chromadb

from emush_rag.models.document import Document, DocumentMetadata
from emush_rag.ports.vector_store import VectorStore

ChromaMetadata = Dict[str, Union[str, int, float, bool]]


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_directory: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(collection_name)

    def index_documents(self, documents: list[Document]) -> None:
        if not documents:
            return

        self.collection.add(
            documents=[doc.content for doc in documents],
            metadatas=[cast(ChromaMetadata, doc.metadata) for doc in documents],
            ids=[document.generate_id() for document in documents],
        )

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
