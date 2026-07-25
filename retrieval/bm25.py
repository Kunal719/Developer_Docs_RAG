from retrieval.base import BaseRetriever
from langchain_community.retrievers import BM25Retriever as LangChainBM25
from langchain_core.documents import Document

class BM25Retriever(BaseRetriever):
    def __init__(self, bm25_index: LangChainBM25):
        self._bm25_index = bm25_index

    def retrieve(self, query: str) -> list[Document]:
        """
        Retrieve the most relevant documents using BM25
        
        Args:
            query: Query string
        
        Returns:
            List of retrieved documents
        """
        return self._bm25_index.invoke(query)