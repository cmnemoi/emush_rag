from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class ChatMessage:
    role: str
    content: str


class LLMClient(ABC):
    @abstractmethod
    def complete(self, system_prompt: str, messages: List[ChatMessage]) -> str:
        pass
