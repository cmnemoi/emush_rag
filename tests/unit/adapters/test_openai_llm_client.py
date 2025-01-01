from unittest.mock import Mock, patch

import pytest

from emush_rag.adapters.openai_llm_client import OpenAILLMClient
from emush_rag.ports.llm_client import ChatMessage
from emush_rag.prompts import SYSTEM_PROMPT, USER_PROMPT


class TestOpenAILLMClient:
    def setup_method(self):
        self.patcher = patch("emush_rag.adapters.openai_llm_client.OpenAI")
        self.mock_openai = self.patcher.start()

        self.mock_client = Mock()
        self.mock_openai.return_value = self.mock_client

        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        self.mock_client.chat.completions.create.return_value = mock_response

        self.llm_client = OpenAILLMClient(model="gpt-4")

        self.sample_chat_history = [
            ChatMessage(role="user", content="Hi"),
            ChatMessage(role="assistant", content="Hello!"),
        ]

        self.sample_context = "Some context"
        self.sample_question = "What is eMush?"

        self.sample_messages = [
            ChatMessage(role="system", content="context"),
            ChatMessage(role="user", content="chat message"),
            ChatMessage(role="assistant", content="response"),
            ChatMessage(role="user", content="question"),
        ]

    def teardown_method(self):
        self.patcher.stop()

    def test_given_chat_messages_when_completing_then_formats_messages_with_prompts(self):
        # Given
        raw_messages = [
            ChatMessage(role="system", content=self.sample_context),
            *self.sample_chat_history,
            ChatMessage(role="user", content=self.sample_question),
        ]

        expected_messages = [
            {"role": "system", "content": SYSTEM_PROMPT.format(context=self.sample_context)},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    question=self.sample_question,
                    chat_history="User: Hi\nAssistant: Hello!",
                ),
            },
        ]

        # When
        self.llm_client.complete(raw_messages)

        # Then
        self.mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4",
            messages=expected_messages,
            seed=OpenAILLMClient.SEED,
            temperature=OpenAILLMClient.TEMPERATURE,
        )

    @pytest.mark.parametrize(
        "message,expected_format",
        [
            (ChatMessage(role="user", content="Hi"), "User: Hi"),
            (ChatMessage(role="assistant", content="Hello!"), "Assistant: Hello!"),
        ],
    )
    def test_given_chat_message_when_formatting_then_returns_formatted_entry(self, message, expected_format):
        # When
        formatted_entry = self.llm_client._format_chat_history_entry(message)

        # Then
        assert formatted_entry == expected_format

    @pytest.mark.parametrize(
        "message,expected_role",
        [
            (ChatMessage(role="system", content="context"), "system"),
            (ChatMessage(role="user", content="question"), "last_user"),
            (ChatMessage(role="user", content="chat message"), "chat_user"),
            (ChatMessage(role="assistant", content="response"), "chat_assistant"),
        ],
    )
    def test_given_message_when_classifying_then_returns_correct_role(self, message, expected_role):
        # When
        role = self.llm_client._classify_message_role(message, self.sample_messages)

        # Then
        assert role == expected_role

    def test_given_context_and_chat_history_when_formatting_then_returns_formatted_messages(self):
        # Given
        chat_history = ["User: Hi", "Assistant: Hello!"]

        # When
        formatted_messages = self.llm_client._create_formatted_messages(
            self.sample_context, self.sample_question, chat_history
        )

        # Then
        assert formatted_messages == [
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(context=self.sample_context),
            },
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    question=self.sample_question,
                    chat_history="\n".join(chat_history),
                ),
            },
        ]
