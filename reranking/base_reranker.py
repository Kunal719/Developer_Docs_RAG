from abc import abstractmethod, ABC
from langchain_core.documents import Document

class BaseReranker(ABC):
    """
    The base class for all rerankers
    """

    @abstractmethod
    def rerank(self, query: str, documents: list[Document]) -> list[Document]:
        ...