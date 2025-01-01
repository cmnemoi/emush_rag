from dataclasses import dataclass
from typing import List, Literal

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from emush_rag.ports.llm_client import ChatMessage, LLMClient
from emush_rag.prompts import SYSTEM_PROMPT, USER_PROMPT


@dataclass
class FormattedMessage:
    role: Literal["system", "user"]
    content: str

    def to_dict(self) -> ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam:
        if self.role == "system":
            return {"role": "system", "content": self.content}
        return {"role": "user", "content": self.content}


class OpenAILLMClient(LLMClient):
    SEED = 42
    TEMPERATURE = 0

    def __init__(self, model: str):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1")
        self.model = model

    def complete(self, messages: List[ChatMessage]) -> str:
        formatted_messages = self._format_messages(messages)
        return self._get_completion_response(formatted_messages)

    def _format_messages(self, messages: List[ChatMessage]) -> List[ChatCompletionMessageParam]:
        if not messages:
            return []

        context = ""
        chat_history = []
        question = ""

        for msg in messages:
            role = self._classify_message_role(msg, messages)
            if role == "system":
                context = msg.content
            elif role == "last_user":
                question = msg.content
            elif role in ["chat_user", "chat_assistant"]:
                chat_history.append(self._format_chat_history_entry(msg))

        return self._create_formatted_messages(context, question, chat_history)

    def _get_completion_response(self, formatted_messages: List[ChatCompletionMessageParam]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=self.TEMPERATURE,
            seed=self.SEED,
        )
        if not response.choices[0].message.content:
            raise ValueError("No response content received from OpenAI")

        return response.choices[0].message.content

    def _classify_message_role(self, message: ChatMessage, messages: List[ChatMessage]) -> str:
        if message.role == "system":
            return "system"
        if message.role == "assistant":
            return "chat_assistant"
        if message.role == "user":
            return "last_user" if message == messages[-1] else "chat_user"
        return "unknown"

    def _create_formatted_messages(
        self, context: str, question: str, chat_history: List[str]
    ) -> List[ChatCompletionMessageParam]:
        system_message = FormattedMessage(
            role="system",
            content=SYSTEM_PROMPT.format(context=context),
        )
        user_message = FormattedMessage(
            role="user",
            content=USER_PROMPT.format(
                question=question,
                chat_history="\n".join(chat_history) if chat_history else "No chat history",
            ),
        )

        return [system_message.to_dict(), user_message.to_dict()]

    def _format_chat_history_entry(self, message: ChatMessage) -> str:
        prefix = "User" if message.role == "user" else "Assistant"
        return f"{prefix}: {message.content}"
