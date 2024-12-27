import json
import shutil
import tempfile
from pathlib import Path

from click.testing import Result
from typer.testing import CliRunner

from emush_rag.adapters.chroma_vector_store import ChromaVectorStore
from emush_rag.cli.index_documents import app


class TestIndexDocumentsCLI:
    def setup_method(self) -> None:
        self.sample_documents = self._create_sample_documents()
        self.temp_dir = self._create_temp_dir()
        self.data_dir = self._create_data_dir()
        self.chroma_persist_dir = self._create_chroma_persist_dir()
        self._write_sample_documents_to_file()

    def teardown_method(self) -> None:
        self._cleanup_temp_directories()

    def test_should_index_json_files_from_data_folder(self) -> None:
        # Given a CLI runner
        runner = self._create_cli_runner()

        # When indexing documents using the CLI
        result = self._run_index_documents_command(runner, collection_name="my_collection")

        # Then the command should succeed
        self._assert_command_succeeded(result)

        # And documents should be stored in Chroma
        indexed_documents = self._get_indexed_documents(collection_name="my_collection")
        self._assert_documents_were_indexed_correctly(indexed_documents)

    def test_should_use_custom_collection_name_when_provided(self) -> None:
        # Given a CLI runner and a custom collection name
        runner = self._create_cli_runner()
        custom_collection_name = "my_custom_collection"

        # When indexing documents using the CLI with a custom collection name
        result = self._run_index_documents_command(runner, collection_name=custom_collection_name)

        # Then the command should succeed
        self._assert_command_succeeded(result)

        # And documents should be stored in Chroma with the custom collection name
        vector_store = ChromaVectorStore(
            persist_directory=str(self.chroma_persist_dir),
            collection_name=custom_collection_name,
        )
        assert vector_store.collection.name == custom_collection_name

    def _create_sample_documents(self) -> list[dict]:
        return [
            {
                "title": "Test 1",
                "content": "This is test document 1",
                "link": "http://example.com/1",
                "source": "test",
            },
            {
                "title": "Test 2",
                "content": "This is test document 2",
                "link": "http://example.com/2",
                "source": "test",
            },
        ]

    def _create_temp_dir(self) -> str:
        return tempfile.mkdtemp()

    def _create_data_dir(self) -> Path:
        data_dir = Path(self.temp_dir) / "data"
        data_dir.mkdir()
        return data_dir

    def _create_chroma_persist_dir(self) -> Path:
        chroma_persist_dir = Path(self.temp_dir) / "chroma"
        chroma_persist_dir.mkdir()
        return chroma_persist_dir

    def _write_sample_documents_to_file(self) -> None:
        with open(self.data_dir / "documents.json", "w") as f:
            json.dump(self.sample_documents, f)

    def _cleanup_temp_directories(self) -> None:
        shutil.rmtree(self.temp_dir)

    def _create_cli_runner(self) -> CliRunner:
        return CliRunner()

    def _run_index_documents_command(self, runner: CliRunner, collection_name: str) -> Result:
        args = ["--data-dir", str(self.data_dir), "--chroma-persist-dir", str(self.chroma_persist_dir)]
        if collection_name:
            args.extend(["--collection-name", collection_name])
        return runner.invoke(app, args)

    def _assert_command_succeeded(self, result: Result) -> None:
        assert result.exit_code == 0
        assert "2 documents indexed successfully!" in result.stdout

    def _get_indexed_documents(self, collection_name: str) -> list:
        vector_store = ChromaVectorStore(
            persist_directory=str(self.chroma_persist_dir),
            collection_name=collection_name,
        )
        return vector_store.get_all_documents()

    def _assert_documents_were_indexed_correctly(self, indexed_documents: list) -> None:
        assert len(indexed_documents) == len(self.sample_documents)
        assert all(doc.metadata["title"] in [d["title"] for d in self.sample_documents] for doc in indexed_documents)
