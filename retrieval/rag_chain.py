from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.language_models.chat_models import BaseChatModel
from prompt.rag_prompt import rag_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from utils.document_formatter import format_retrieved_context

def build_rag_chain(retriever: VectorStoreRetriever, llm: BaseChatModel, prompt: ChatPromptTemplate = rag_prompt):
    """
    Build the end-to-end Retrieval-Augmented Generation (RAG) chain.

    Args:
        retriever: Configured retriever used to fetch relevant documents.
        llm: Chat language model used for answer generation.
        prompt: Prompt template for the RAG pipeline.

    Returns:
        A runnable LCEL RAG chain.
    """

    chain = (
        {
            "context": retriever | RunnableLambda(format_retrieved_context),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain