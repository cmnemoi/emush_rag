import os
from dataclasses import dataclass


@dataclass
class Config:
    chat_model: str = "gpt-4o-mini"
    collection_name: str = "emush_rag_lite"
    chroma_db_directory: str = "chroma"
    data_directory: str = "data"
    embedding_model: str = "text-embedding-3-large"
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
