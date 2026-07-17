from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from pathlib import Path

def load_documents(docs_path: Path) -> list[Document]:
    """
    Load Markdown and MDX files from the documentation directory
    and return them as LangChain Document objects.

    Args:
        docs_path: The path to the documentation directory.

    Returns:
        A list of LangChain Document objects.
    """
    loader = DirectoryLoader(
        path=docs_path,
        glob="**/*.mdx",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    return loader.load()