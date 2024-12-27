from emush_rag.models.document import Document, DocumentMetadata
from emush_rag.usecases.index_documents import IndexDocuments
from tests.test_doubles import FakeVectorStore
from tests.test_doubles.test_doubles import InMemoryJsonDocumentReader


class TestIndexDocuments:
    def setup_method(self):
        self.document_reader = InMemoryJsonDocumentReader()
        self.vector_store = FakeVectorStore()
        self.index_documents = IndexDocuments(document_reader=self.document_reader, vector_store=self.vector_store)

    def test_list_of_two_documents_should_be_indexed_in_vector_store(self):
        documents = self._create_documents(2)
        self.index_documents.execute()
        self._assert_documents_indexed(documents)

    def test_list_of_eleven_documents_should_be_indexed_by_batches_of_ten_documents(self):
        self._create_documents(11)
        self.index_documents.execute()
        self._assert_batch_count(2)

    def test_list_of_one_document_with_1000_characters_should_be_indexed_by_batches_of_2_documents_of_500_characters(
        self,
    ):
        self._create_documents(1, content="a" * 1000)
        self.index_documents.execute()
        self._assert_batch_count(2)

    def test_list_of_two_documents_with_1000_characters_should_be_indexed_by_batches_of_4_documents_of_500_characters(
        self,
    ):
        self._create_documents(2, content="a" * 1000)
        self.index_documents.execute()
        self._assert_batch_count(4)

    def _create_documents(self, count: int, content="azaza") -> list[Document]:
        documents = [self._create_document(title_suffix=f"-{i}", content=content) for i in range(1, count + 1)]
        self.document_reader.set_json_entries(documents)
        return documents

    def _create_document(self, title_suffix="", content="azaza") -> Document:
        return Document(
            content=content,
            metadata=DocumentMetadata(
                title=f"title{title_suffix}",
                link=f"https://example{title_suffix}.com",
                source=f"source{title_suffix}",
            ),
        )

    def _assert_documents_indexed(self, documents):
        assert self.vector_store.get_all() == documents

    def _assert_batch_count(self, expected_batch_count):
        self.vector_store.should_be_called_times(expected_batch_count)
