import os
from dataclasses import dataclass


@dataclass
class Config:
    chat_model: str = "gpt-4o-mini"
    collection_name: str = "emush_rag_lite"
    chroma_db_directory: str = "chroma"
    data_directory: str = "data"
    embedding_model: str = "text-embedding-3-large"
    evaluation_model: str = "gpt-4o-mini"
    indexation_batch_size: int = 100
    indexation_nb_characters_per_document: int = 1_000
    max_relevant_documents: int = 5
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
