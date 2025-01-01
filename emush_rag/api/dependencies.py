from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction

from emush_rag.adapters.chroma_vector_store import ChromaVectorStore
from emush_rag.adapters.openai_llm_client import OpenAILLMClient
from emush_rag.config import Config
from emush_rag.usecases.answer_user_question import AnswerUserQuestion

config = Config()


def answer_user_question() -> AnswerUserQuestion:
    return AnswerUserQuestion(llm_client=_llm_client(), vector_store=_vector_store(_embedding_function()))


def _llm_client() -> OpenAILLMClient:
    return OpenAILLMClient(model=config.chat_model)


def _vector_store(embedding_function: OpenAIEmbeddingFunction) -> ChromaVectorStore:
    return ChromaVectorStore(
        persist_directory=config.chroma_db_directory,
        collection_name=config.collection_name,
        embedding_function=embedding_function,
    )


def _embedding_function() -> OpenAIEmbeddingFunction:
    return OpenAIEmbeddingFunction(api_key=config.openai_api_key, model_name=config.embedding_model)
