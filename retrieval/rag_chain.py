from retrieval.base import BaseRetriever
from langchain_core.language_models.chat_models import BaseChatModel
from prompt.rag_prompt import rag_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from utils.document_formatter import format_retrieved_context

def build_rag_chain(retriever: BaseRetriever, llm: BaseChatModel, prompt: ChatPromptTemplate = rag_prompt):
    """
    Build the end-to-end Retrieval-Augmented Generation (RAG) chain.

    Args:
        retriever: Configured retriever used to fetch relevant documents.
        llm: Chat language model used for answer generation.
        prompt: Prompt template for the RAG pipeline.

    Returns:
        A runnable LCEL RAG chain.
    """

    retrieve_documents = RunnableLambda(lambda query: retriever.retrieve(query))
    format_documents = RunnableLambda(lambda docs: format_retrieved_context(docs))

    chain = (
        {
            "context":  retrieve_documents | format_documents,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain