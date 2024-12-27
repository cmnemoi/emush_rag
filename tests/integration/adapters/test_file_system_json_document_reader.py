from emush_rag.adapters.file_system_json_document_reader import FileSystemJsonDocumentReader
from emush_rag.models.document import Document


class TestFileSystemJsonDocumentReader:
    """Test suite for FileSystemJsonDocumentReader adapter"""

    def setup_method(self):
        """Set up a fresh reader instance for each test"""
        self.reader = FileSystemJsonDocumentReader(data_directory="tests/integration/adapters/data")

    def test_should_read_at_least_one_json_file_from_data_directory(self):
        json_entries = self._when_reading_json_entries()

        self._then_should_have_at_least_one_entry(json_entries)

    def test_should_return_json_entries_with_required_fields(self):
        json_entries = self._when_reading_json_entries()

        self._then_all_entries_should_have_required_fields(json_entries)

    def _when_reading_json_entries(self) -> list[Document]:
        return self.reader.read_documents()

    def _then_should_have_at_least_one_entry(self, json_entries: list[Document]) -> None:
        assert len(json_entries) > 0, "Expected at least one JSON entry to be read from the data directory"

    def _then_all_entries_should_have_required_fields(self, json_entries: list[dict]) -> None:
        for entry in json_entries:
            self._then_entry_should_be_a_document(entry)

    def _then_entry_should_be_a_document(self, entry: dict) -> None:
        assert isinstance(entry, Document), "Each entry should be a Document"
