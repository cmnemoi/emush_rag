from pydantic import BaseModel

from emush_rag.ports.llm_client import ChatMessage


class QuestionRequest(BaseModel):
    question: str
    chat_history: list[ChatMessage] = []


class QuestionResponse(BaseModel):
    answer: str
