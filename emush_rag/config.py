import os
from dataclasses import dataclass


@dataclass
class Config:
    chat_model: str = "gpt-4.1-mini"
    collection_name: str = "emush_rag_lite"
    chroma_db_directory: str = "chroma"
    data_directory: str = "data"
    embedding_model: str = "text-embedding-3-large"
    evaluation_model: str = "gpt-4o-mini"
    rate_limit_max_requests: int = 100
    rate_limit_window_seconds: int = 60
    indexation_batch_size: int = 100
    indexation_nb_characters_per_document: int = 1_000
    max_relevant_documents: int = 5
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    vector_store_url: str = os.getenv("VECTOR_STORE_URL", default="vector_store")
    vector_store_port: int = int(os.getenv("VECTOR_STORE_PORT", default=8000))
