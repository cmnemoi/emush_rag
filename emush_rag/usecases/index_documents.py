from tqdm import tqdm

from emush_rag.models.document import Document
from emush_rag.ports.document_reader import DocumentReader
from emush_rag.ports.vector_store import VectorStore


class IndexDocuments:
    """
    Use case to index documents in the vector store. It splits large documents into smaller chunks before indexing them.
    """

    def __init__(
        self,
        document_reader: DocumentReader,
        vector_store: VectorStore,
        batch_size: int = 10,
        nb_characters_per_document: int = 500,
    ):
        self.document_reader = document_reader
        self.vector_store = vector_store
        self.batch_size = batch_size
        self.nb_characters_per_document = nb_characters_per_document

    def execute(self) -> None:
        """
        Index documents in the vector store. Large documents are split into smaller chunks before indexing them.
        """
        documents = self.document_reader.read_documents()
        small_documents = []
        for document in tqdm(documents, desc="Indexing large documents chunks"):
            if self._is_document_large(document):
                self._index_large_document(document)
            else:
                small_documents.append(document)

        self._index_small_documents(small_documents)

    def _is_document_large(self, document: Document) -> bool:
        return document.length() > self.nb_characters_per_document

    def _index_large_document(self, document: Document) -> None:
        chunks = self._split_document_content_into_chunks(document)
        for chunk in chunks:
            doc = Document(content=chunk, metadata=document.metadata)
            self.vector_store.index_documents([doc])

    def _split_document_content_into_chunks(self, document: Document) -> list[str]:
        return [
            document.content[i : i + self.nb_characters_per_document]
            for i in range(0, document.length(), self.nb_characters_per_document)
        ]

    def _index_small_documents(self, documents: list[Document]) -> None:
        for i in tqdm(range(0, len(documents), self.batch_size), desc="Indexing small documents batches"):
            self.vector_store.index_documents(documents[i : i + self.batch_size])
