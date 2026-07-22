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

def load_selected_documents(selected_docs_relative_path: set[str], docs_path: Path) -> list[Document]:
    """
    Load only the selected documents from the documentation directory
    and return them as LangChain Document objects.

    Args:
        selected_docs_relative_path: The relative path to the selected document.
        docs_path: The path to the documentation directory.

    Returns:
        A list of LangChain Document objects.
    """
    documents = []

    for doc in selected_docs_relative_path:
        doc_full_path = docs_path / doc

        if doc_full_path.is_file():
            loader = TextLoader(str(doc_full_path), encoding="utf-8")
            documents.extend(loader.load())
    
    return documents