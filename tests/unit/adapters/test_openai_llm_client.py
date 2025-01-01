from unittest.mock import Mock, patch

import pytest

from emush_rag.adapters.openai_llm_client import OpenAILLMClient
from emush_rag.ports.llm_client import ChatMessage
from emush_rag.prompts import SYSTEM_PROMPT, USER_PROMPT


@pytest.fixture
def mock_openai():
    with patch("emush_rag.adapters.openai_llm_client.OpenAI") as mock:
        yield mock


@pytest.fixture
def mock_openai_client(mock_openai):
    mock_client = Mock()
    mock_openai.return_value = mock_client

    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Test response"))]
    mock_client.chat.completions.create.return_value = mock_response

    return mock_client


@pytest.fixture
def llm_client():
    return OpenAILLMClient(model="gpt-4")


def test_complete_should_format_messages_with_prompts(mock_openai_client, llm_client):
    # Given
    context = "Some context"
    question = "What is eMush?"
    chat_history = [
        ChatMessage(role="user", content="Hi"),
        ChatMessage(role="assistant", content="Hello!"),
    ]

    raw_messages = [
        ChatMessage(role="system", content=context),
        *chat_history,
        ChatMessage(role="user", content=question),
    ]

    expected_messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        {
            "role": "user",
            "content": USER_PROMPT.format(
                question=question,
                chat_history="User: Hi\nAssistant: Hello!",
            ),
        },
    ]

    # When
    llm_client.complete(raw_messages)

    # Then
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=expected_messages,
        seed=OpenAILLMClient.SEED,
        temperature=OpenAILLMClient.TEMPERATURE,
    )


def test_format_chat_history_entry(mock_openai, llm_client):
    # Given
    user_message = ChatMessage(role="user", content="Hi")
    assistant_message = ChatMessage(role="assistant", content="Hello!")

    # When
    user_entry = llm_client._format_chat_history_entry(user_message)
    assistant_entry = llm_client._format_chat_history_entry(assistant_message)

    # Then
    assert user_entry == "User: Hi"
    assert assistant_entry == "Assistant: Hello!"


def test_classify_message_role(mock_openai, llm_client):
    # Given
    system_message = ChatMessage(role="system", content="context")
    last_user_message = ChatMessage(role="user", content="question")
    chat_user_message = ChatMessage(role="user", content="chat message")
    assistant_message = ChatMessage(role="assistant", content="response")

    messages = [system_message, chat_user_message, assistant_message, last_user_message]

    # When/Then
    assert llm_client._classify_message_role(system_message, messages) == "system"
    assert llm_client._classify_message_role(last_user_message, messages) == "last_user"
    assert llm_client._classify_message_role(chat_user_message, messages) == "chat_user"
    assert llm_client._classify_message_role(assistant_message, messages) == "chat_assistant"


def test_create_formatted_messages(mock_openai, llm_client):
    # Given
    context = "Some context"
    question = "What is eMush?"
    chat_history = ["User: Hi", "Assistant: Hello!"]

    # When
    formatted_messages = llm_client._create_formatted_messages(context, question, chat_history)

    # Then
    assert formatted_messages == [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        {
            "role": "user",
            "content": USER_PROMPT.format(
                question=question,
                chat_history="\n".join(chat_history),
            ),
        },
    ]
