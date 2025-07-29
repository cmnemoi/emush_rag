from dataclasses import dataclass
from typing import List, Literal

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from emush_rag.ports.llm_client import ChatMessage, LLMClient


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
        self.client = OpenAI()
        self.model = model

    def complete(self, system_prompt: str, messages: List[ChatMessage]) -> str:
        formatted_messages = self._format_messages(system_prompt, messages)
        return self._get_completion_response(formatted_messages)

    def _format_messages(self, system_prompt: str, messages: List[ChatMessage]) -> List[ChatCompletionMessageParam]:
        if not messages:
            return []

        context = ""
        question = ""

        for msg in messages:
            role = self._classify_message_role(msg, messages)
            if role == "system":
                context = msg.content
            elif role == "last_user":
                question = msg.content

        return self._create_formatted_messages(system_prompt, context, question)

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
        self, system_prompt: str, context: str, question: str
    ) -> List[ChatCompletionMessageParam]:
        system_message = FormattedMessage(
            role="system",
            content=system_prompt.format(context=context),
        )
        user_message = FormattedMessage(
            role="user",
            content=question,
        )

        return [system_message.to_dict(), user_message.to_dict()]
