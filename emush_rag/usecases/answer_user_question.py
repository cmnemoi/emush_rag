from emush_rag.ports.llm_client import ChatMessage, LLMClient
from emush_rag.ports.vector_store import VectorStore


class AnswerUserQuestion:
    def __init__(self, llm_client: LLMClient, vector_store: VectorStore):
        self.llm_client = llm_client
        self.vector_store = vector_store

    def execute(self, question: str, chat_history: list[ChatMessage]) -> str:
        messages = self._build_messages(question, chat_history)
        return self.llm_client.complete(messages)

    def _build_messages(self, question: str, chat_history: list[ChatMessage]) -> list[ChatMessage]:
        context = self._get_context(question)
        messages = [
            ChatMessage(role="system", content=context),
            *chat_history,
            ChatMessage(role="user", content=question),
        ]

        return messages

    def _get_context(self, question: str) -> str:
        relevant_documents = self.vector_store.get_relevant_documents(question)
        if not relevant_documents:
            return ""

        contexts = []
        for doc in relevant_documents:
            source = doc.metadata.get("source", "unknown source")
            contexts.append(f"[{source}]\n{doc.content}")

        return "\n\n".join(contexts)
