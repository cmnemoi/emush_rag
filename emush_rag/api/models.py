from pydantic import BaseModel

from emush_rag.models.document import Document
from emush_rag.ports.llm_client import ChatMessage


class QuestionRequest(BaseModel):
    question: str = "Est-ce que les alarmes détectent les extirpations de spores ?"
    chat_history: list[ChatMessage] = []


class QuestionResponse(BaseModel):
    answer: str
    retrieved_documents: list[Document] = []
