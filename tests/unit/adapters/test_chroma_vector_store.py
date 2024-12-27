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

    def _given_a_document_with_metadata(self, content: str, metadata: DocumentMetadata) -> Document:
        return Document(content=content, metadata=metadata)

    def _given_document_metadata(self, title: str, link: str, source: str) -> DocumentMetadata:
        return DocumentMetadata(title=title, link=link, source=source)

    def _when_indexing_documents(self, documents: list[Document]) -> None:
        self.store.index_documents(documents)

    def _then_stored_documents_should_match(self, expected_documents: list[Document]) -> None:
        actual_documents = self.store.get_all_documents()
        assert actual_documents == expected_documents
