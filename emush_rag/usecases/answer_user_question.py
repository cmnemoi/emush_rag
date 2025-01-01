from emush_rag.models.document import Document
from emush_rag.ports.llm_client import ChatMessage, LLMClient
from emush_rag.ports.vector_store import VectorStore


class AnswerUserQuestion:
    def __init__(self, llm_client: LLMClient, vector_store: VectorStore):
        self.llm_client = llm_client
        self.vector_store = vector_store

    def execute(
        self, question: str, chat_history: list[ChatMessage], max_relevant_documents: int
    ) -> tuple[str, list[Document]]:
        relevant_documents = self.vector_store.get_relevant_documents(question, max_relevant_documents)
        messages = self._build_messages(question, chat_history, relevant_documents)
        return self.llm_client.complete(messages), relevant_documents

    def _build_messages(
        self, question: str, chat_history: list[ChatMessage], relevant_documents: list[Document]
    ) -> list[ChatMessage]:
        context = self._get_context(relevant_documents)
        messages = [
            ChatMessage(role="system", content=context),
            *chat_history,
            ChatMessage(role="user", content=question),
        ]

        return messages

    def _get_context(self, relevant_documents: list[Document]) -> str:
        if not relevant_documents:
            return ""

        contexts = []
        for doc in relevant_documents:
            source = doc.metadata.get("source", "unknown source")
            contexts.append(f"[{source}]\n{doc.content}")

        return "\n\n".join(contexts)
