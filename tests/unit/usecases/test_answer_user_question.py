from emush_rag.ports.llm_client import ChatMessage
from emush_rag.usecases.answer_user_question import AnswerUserQuestion
from tests.test_doubles.test_doubles import FakeLLMClient, FakeVectorStore


class TestAnswerUserQuestion:
    def setup_method(self) -> None:
        self.llm_client = FakeLLMClient(expected_response="eMush is the greatest space opera.")
        self.vector_store = FakeVectorStore()
        self.usecase = AnswerUserQuestion(llm_client=self.llm_client, vector_store=self.vector_store)

    def test_should_return_llm_response_for_question(self) -> None:
        # Given
        question = "What is eMush?"
        chat_history: list[ChatMessage] = []

        # When
        response = self.usecase.execute(question=question, chat_history=chat_history, max_relevant_documents=1)

        # Then
        assert response == ("eMush is the greatest space opera.", [])
