from abc import abstractmethod, ABC
from langchain_core.documents import Document

class BaseRetriever(ABC):
    """
    Abstract class for all retrievers strategies
    """

    @abstractmethod
    def retrieve(self, query: str) -> list[Document]:
        """
        Retrieve the most relevant documents for given query
        
        Args:
            query: Query string

        Returns:
            List of retrieved documents
        """
        ...