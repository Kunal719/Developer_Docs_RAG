from retrieval.base import BaseRetriever
from langchain_core.documents import Document

class MultiCorpusRetriever(BaseRetriever):

    def __init__(self, retrievers: list[BaseRetriever]):
        self._retrievers = retrievers

    def retrieve(self, query: str) -> list[Document]:
        """
        Retrieve the combined most relevant documents for given query from all retrievers

        Args:
            query: Query string

        Returns:
            List of retrieved documents
        """
        combined_docs = []

        for retriever in self._retrievers:
            combined_docs.extend(retriever.retrieve(query))

        return combined_docs