from langchain_text_splitters import RecursiveCharacterTextSplitter

from emush_rag.models.document import Document
from emush_rag.ports.document_splitter import DocumentSplitter


class LangchainRecursiveCharacterDocumentSplitter(DocumentSplitter):
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, document: Document) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        return [
            Document(content=chunk, metadata=document.metadata) for chunk in text_splitter.split_text(document.content)
        ]
