from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from emush_rag import __version__ as version
from emush_rag.api.dependencies import answer_user_question
from emush_rag.api.models import QuestionRequest, QuestionResponse
from emush_rag.config import Config
from emush_rag.usecases.answer_user_question import AnswerUserQuestion

app = FastAPI(
    title="eMush RAG API",
    description="A RAG-based API to answer questions about eMush.",
    version=version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

config = Config()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    path="/api/questions",
    response_model=QuestionResponse,
)
async def answer_question(
    request: QuestionRequest, usecase: AnswerUserQuestion = Depends(answer_user_question)
) -> QuestionResponse:
    answer, retrieved_documents = usecase.execute(
        request.question, request.chat_history, config.max_relevant_documents
    )
    return QuestionResponse(answer=answer, retrieved_documents=retrieved_documents)
