from langchain_core.documents import Document
from retrieval.base import BaseRetriever
from langchain_chroma import Chroma

class DenseRetriever(BaseRetriever):
    def __init__(self, vector_store: Chroma, top_k: int):
        self._vector_store = vector_store
        self._top_k = top_k

    def retrieve(self, query: str) -> list[Document]:
        """
        Retrieve the most relevant documents using Dense Retriever

        Args:
            query: Query string

        Returns:
            List of retrieved documents
        """
        retriever = self._vector_store.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k": self._top_k},
        )

        return retriever.invoke(query)        
