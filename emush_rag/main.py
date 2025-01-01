from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from emush_rag.adapters.chroma_vector_store import ChromaVectorStore
from emush_rag.adapters.openai_llm_client import OpenAILLMClient
from emush_rag.ports.llm_client import ChatMessage
from emush_rag.usecases.answer_user_question import AnswerUserQuestion

load_dotenv()

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str
    chat_history: List[ChatMessage] = []


class QuestionResponse(BaseModel):
    answer: str


def get_answer_user_question_usecase() -> AnswerUserQuestion:
    return AnswerUserQuestion(
        llm_client=OpenAILLMClient(model="gpt-4o-mini"),
        vector_store=ChromaVectorStore(
            persist_directory="chroma",
            collection_name="emush_rag_lite",
        ),
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/questions", response_model=QuestionResponse)
async def answer_question(
    request: QuestionRequest, usecase: AnswerUserQuestion = Depends(get_answer_user_question_usecase)
) -> QuestionResponse:
    answer = usecase.execute(request.question, request.chat_history)
    return QuestionResponse(answer=answer)
