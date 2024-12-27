import typer

from emush_rag.adapters.chroma_vector_store import ChromaVectorStore
from emush_rag.adapters.file_system_json_document_reader import FileSystemJsonDocumentReader
from emush_rag.usecases.index_documents import IndexDocuments

DATA_DIR = "data"
CHROMA_PERSIST_DIR = "chroma"

app = typer.Typer()


@app.command()
def main(
    data_dir: str = typer.Option(DATA_DIR, help="Path to directory containing documents to index"),
    chroma_persist_dir: str = CHROMA_PERSIST_DIR,
    collection_name: str = "",
) -> None:
    """Index JSON documents from data directory into Chroma vector store"""
    document_reader = FileSystemJsonDocumentReader(data_directory=data_dir)
    vector_store = ChromaVectorStore(
        persist_directory=chroma_persist_dir,
        collection_name=collection_name,
    )

    index_documents_usecase = IndexDocuments(
        document_reader=document_reader,
        vector_store=vector_store,
    )
    index_documents_usecase.execute()

    indexed_documents = vector_store.get_all_documents()
    typer.echo(f"{len(indexed_documents)} documents indexed successfully!")


if __name__ == "__main__":
    app()
