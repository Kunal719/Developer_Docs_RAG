from langchain_openai import OpenAIEmbeddings

def get_embedding_model() -> OpenAIEmbeddings:
    """
    Return the embedding model to be used for generating document embeddings
    """
    return OpenAIEmbeddings(model="text-embedding-3-small")