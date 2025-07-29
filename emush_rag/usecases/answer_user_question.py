from emush_rag.models.document import Document
from emush_rag.ports.llm_client import ChatMessage, LLMClient
from emush_rag.ports.vector_store import VectorStore
from emush_rag.prompts import REFORMULATION_PROMPT, SYSTEM_PROMPT


class AnswerUserQuestion:
    def __init__(self, llm_client: LLMClient, vector_store: VectorStore):
        self.llm_client = llm_client
        self.vector_store = vector_store

    def execute(
        self, question: str, chat_history: list[ChatMessage], max_relevant_documents: int
    ) -> tuple[str, list[Document]]:
        reformulated_question = self._reformulate_question(question, chat_history)

        relevant_documents = self.vector_store.get_relevant_documents(reformulated_question, max_relevant_documents)
        return self.llm_client.complete(
            SYSTEM_PROMPT.format(context=self._get_context(relevant_documents)),
            [
                ChatMessage(role="user", content=reformulated_question),
            ],
        ), relevant_documents

    def _reformulate_question(self, question: str, chat_history: list[ChatMessage]) -> str:
        if not chat_history:
            return question

        conversation = [f"{message.role}: {message.content}" for message in chat_history]
        if f"user: {question}" not in conversation:
            conversation.append(f"user: {question}")

        messages = [
            ChatMessage(
                role="user",
                content=f"Reformulate this conversation:\n{'\n'.join(conversation)}",
            ),
        ]

        return self.llm_client.complete(REFORMULATION_PROMPT, messages)

    def _get_context(self, relevant_documents: list[Document]) -> str:
        if not relevant_documents:
            return ""

        return "\n\n".join(
            [
                f"[{document.metadata.get('source', 'unknown source')}]\n{document.content}"
                for document in relevant_documents
            ]
        )
