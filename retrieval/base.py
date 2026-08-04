from abc import abstractmethod, ABC
from langchain_core.documents import Document
from evaluation.observer import PipelineObserver

class BaseRetriever(ABC):
    """
    Abstract class for all retrievers strategies
    """

    @abstractmethod
    def retrieve(self, query: str, observer: PipelineObserver | None = None) -> list[Document]:
        """
        Retrieve the most relevant documents for given query
        
        Args:
            query: Query string

        Returns:
            List of retrieved documents
        """
        ...