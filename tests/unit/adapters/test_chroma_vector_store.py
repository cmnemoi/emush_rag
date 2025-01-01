import shutil
import tempfile

from emush_rag.adapters.chroma_vector_store import ChromaVectorStore
from emush_rag.models.document import Document, DocumentMetadata


class TestChromaVectorStore:
    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.store = ChromaVectorStore(
            persist_directory=self.temp_dir,
            collection_name="my_collection",
        )

    def teardown_method(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_document_metadata_is_converted_to_chroma_compatible_format(self) -> None:
        document = self._given_a_document_with_metadata(
            content="test content",
            metadata=self._given_document_metadata(title="test title", link="test link", source="test source"),
        )

        self._when_indexing_documents([document])

        self._then_stored_documents_should_match([document])

    def test_get_relevant_documents_extracts_documents_from_query_results(self) -> None:
        documents = self._given_sample_documents()
        self._when_indexing_documents(documents)

        relevant_documents = self._when_getting_relevant_documents("test query")

        self._then_documents_should_be_valid(relevant_documents)
        self._then_documents_should_match_original(relevant_documents, documents)

    def _given_sample_documents(self) -> list[Document]:
        return [
            self._given_a_document_with_metadata(
                content=f"test content {i}",
                metadata=self._given_document_metadata(
                    title=f"test title {i}", link=f"test link {i}", source=f"test source {i}"
                ),
            )
            for i in range(1, 3)
        ]

    def _given_a_document_with_metadata(self, content: str, metadata: DocumentMetadata) -> Document:
        return Document(content=content, metadata=metadata)

    def _given_document_metadata(self, title: str, link: str, source: str) -> DocumentMetadata:
        return DocumentMetadata(title=title, link=link, source=source)

    def _when_indexing_documents(self, documents: list[Document]) -> None:
        self.store.index_documents(documents)

    def _when_getting_relevant_documents(self, query: str) -> list[Document]:
        return self.store.get_relevant_documents(query)

    def _then_stored_documents_should_match(self, expected_documents: list[Document]) -> None:
        actual_documents = self.store.get_all_documents()
        assert actual_documents == expected_documents

    def _then_documents_should_be_valid(self, documents: list[Document]) -> None:
        assert len(documents) == 2
        assert all(isinstance(doc, Document) for doc in documents)
        for doc in documents:
            self._then_document_metadata_should_be_valid(doc)

    def _then_document_metadata_should_be_valid(self, document: Document) -> None:
        assert "title" in document.metadata
        assert "link" in document.metadata
        assert "source" in document.metadata

    def _then_documents_should_match_original(
        self, actual_documents: list[Document], expected_documents: list[Document]
    ) -> None:
        assert all(doc in expected_documents for doc in actual_documents)
