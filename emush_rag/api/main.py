from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

from emush_rag import __version__
from emush_rag.api.dependencies import answer_user_question, rate_limiter
from emush_rag.api.middleware import RateLimitMiddleware
from emush_rag.api.models import QuestionRequest, QuestionResponse
from emush_rag.api.observability import tracer_provider
from emush_rag.config import Config
from emush_rag.usecases.answer_user_question import AnswerUserQuestion

app = FastAPI(
    title="eMush RAG API",
    description="A RAG-based API to answer questions about eMush.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://askneron.netlify.app",
        "https://emush.eternaltwin.org",
        "https://staging.emush.eternaltwin.org",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
    max_age=3_600,
)

app.add_middleware(
    RateLimitMiddleware,
    rate_limiter=rate_limiter(),
)

config = Config()

FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/version")
async def get_version():
    return {"version": __version__}


@app.post(
    path="/api/questions",
    response_model=QuestionResponse,
)
async def answer_question(
    request: QuestionRequest,
    usecase: AnswerUserQuestion = Depends(answer_user_question),
) -> QuestionResponse:
    try:
        answer, retrieved_documents = usecase.execute(
            request.question, request.chat_history, config.max_relevant_documents
        )
        return QuestionResponse(answer=answer, retrieved_documents=retrieved_documents)
    except Exception as error:
        trace.get_current_span().record_exception(error)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error))
