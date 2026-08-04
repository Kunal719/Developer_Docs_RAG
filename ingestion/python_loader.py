from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from pathlib import Path

def load_python_documents(docs_path: Path) -> list[Document]:
    """
    Load Python files from a directory recursively and return them as LangChain Document objects.

    Args:
        docs_path: Path containing the Python implementation files.
    
    Returns:
        A list of LangChain Document objects.
    """

    loader = DirectoryLoader(
        path=docs_path,
        glob="**/*.py",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    return loader.load()

def load_selected_python_documents(selected_sources_relative_path: set[str], code_path: Path) -> list[Document]:
    """
    Load only the selected documents from the implemetation directory
    and return them as LangChain Document objects.

    Args:
        selected_docs_relative_path: The relative path to the selected document.
        docs_path: The path to the implementation directory.

    Returns:
        A list of LangChain Document objects.
    """
    documents = []

    for doc in selected_sources_relative_path:
        doc_full_path = code_path / doc

        if doc_full_path.is_file():
            loader = TextLoader(str(doc_full_path), encoding="utf-8")
            documents.extend(loader.load())
    
    return documents