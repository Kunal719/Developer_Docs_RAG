from langchain_openai import OpenAIEmbeddings
from config import EMBEDDING_MODEL

def get_embedding_model() -> OpenAIEmbeddings:
    """
    Return the embedding model to be used for generating document embeddings
    """
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)