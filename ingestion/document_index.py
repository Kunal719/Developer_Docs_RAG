from pathlib import Path
import hashlib
import json
from dataclasses import dataclass

@dataclass
class ChangeSet:
    new: set[str]
    deleted: set[str]
    updated: set[str]
    has_changes: bool


def discover_documents(docs_path: Path) -> list[Path]:
    """
    Return a list of MDX files in the mentioned directory. We sort them for consistency

    Args:
        docs_path: The path to the documentation directory.

    Returns:
        A list of MDX files.
    """
    return sorted(list(docs_path.glob("**/*.mdx")))

def compute_sha256(file_path: Path, chunk_size=65536) -> str:
    """
    Hashes the document, chunk by chunk using SHA-256
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    
    return sha256.hexdigest()

def load_index_metadata(index_path: Path) -> dict:
    """
    Load the metadata index if it exists, otherwise create a .json file and return an empty dict

    Args:
        index_path: The path to the metadata index file.

    Returns:
        A dictionary containing the metadata index. 
    """
    if index_path.exists():
        return json.loads(index_path.read_text(encoding="utf-8"))
    else:
        # Create the file
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text("{}", encoding="utf-8")
        return {}

def detect_changes(docs_path: Path,  index_path: Path) -> ChangeSet:
    """
    Detect changes in the documentation directory and return a list of new, deleted, and updated files.

    Args:
        docs_path: The path to the documentation directory.
        index_path: The path to the metadata index file.

    Returns:
        A ChangeSet object containing the new, deleted, and updated files.
    """

    changes_detected : bool = False
    current_docs = discover_documents(docs_path)

    # Map relative path to full path
    current_files = {
        doc.relative_to(docs_path).as_posix(): doc for doc in current_docs
    }

    # Load current index metadata
    index_metadata = load_index_metadata(index_path)

    current_paths = set(current_files.keys())
    indexed_paths = set(index_metadata.keys())

    new_files = current_paths - indexed_paths
    deleted_files = indexed_paths - current_paths
    common_files = current_paths & indexed_paths


    updated_files = set()
    for relative_path in common_files:
        full_path = current_files[relative_path]

        if compute_sha256(full_path) != index_metadata[relative_path]:
            updated_files.add(relative_path)
    
    if new_files or deleted_files or updated_files:
        changes_detected = True
            
    return ChangeSet(new=new_files, deleted=deleted_files, updated=updated_files, has_changes=changes_detected)

def update_index_metadata(index_path: Path, change_set: ChangeSet, docs_path: Path) -> None:
    """
    Update the metadata index to reflect the current indexed documents.

    Args:
        index_path: The path to the metadata index file.
        change_set: A ChangeSet object containing the new, deleted, and updated files.
        docs_path: The path to the documentation directory.
    """

    index_metadata = load_index_metadata(index_path)

    # Add new documents
    for relative_path in change_set.new:
        full_path = docs_path / relative_path
        index_metadata[relative_path] = compute_sha256(full_path)
    
    # Update existing documents
    for relative_path in change_set.updated:
        full_path = docs_path / relative_path
        index_metadata[relative_path] = compute_sha256(full_path)
    
    # Delete the documents
    for relative_path in change_set.deleted:
        index_metadata.pop(relative_path, None)

    index_path.write_text(json.dumps(index_metadata, indent=2, sort_keys=True), encoding="utf-8")
    