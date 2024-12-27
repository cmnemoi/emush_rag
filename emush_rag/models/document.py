import uuid
from dataclasses import dataclass
from typing import TypedDict

DocumentMetadata = TypedDict("DocumentMetadata", {"title": str, "link": str, "source": str})


@dataclass
class Document:
    """
    Document model. It contains the content of the document to index and its metadata (title, link and source).
    """

    content: str
    metadata: DocumentMetadata

    def length(self) -> int:
        return len(self.content)

    def generate_id(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, self._hash()))

    def _hash(self) -> str:
        return str(hash(str(self._to_dict())))

    def _to_dict(self) -> dict:
        return {
            "content": self.content,
            "title": self.metadata["title"],
            "link": self.metadata["link"],
            "source": self.metadata["source"],
        }

    @staticmethod
    def from_dict(dictionary: dict) -> "Document":
        return Document(
            content=dictionary["content"],
            metadata={"title": dictionary["title"], "link": dictionary["link"], "source": dictionary["source"]},
        )
