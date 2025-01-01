import typer
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction

from emush_rag.adapters.chroma_vector_store import ChromaVectorStore
from emush_rag.adapters.file_system_json_document_reader import FileSystemJsonDocumentReader
from emush_rag.config import Config
from emush_rag.usecases.index_documents import IndexDocuments

app = typer.Typer()
config = Config()


@app.command()
def main(
    data_dir: str = typer.Option(config.data_directory, help="Path to directory containing documents to index"),
    chroma_persist_dir: str = config.chroma_db_directory,
    collection_name: str = config.collection_name,
) -> None:
    """Index JSON documents from data directorya into Chroma vector store"""
    document_reader = FileSystemJsonDocumentReader(data_directory=data_dir)
    vector_store = ChromaVectorStore(
        persist_directory=chroma_persist_dir,
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddingFunction(api_key=config.openai_api_key, model_name=config.embedding_model),
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
