# # Clone or Pull the repository based on if it is already cloned or needs to be pulled
# from pathlib import Path

# from git import Repo
# from git.exc import GitCommandError, InvalidGitRepositoryError

# def load_repository(repo_url: str, local_path: Path) -> Path:
#     """
#     Clone the repository if it doesn't exist locally; otherwise update it.
#     Return the local repository path.

#     Args:
#         repo_url (str): The URL of the GitHub repository to clone or update.
#         local_path (Path): The local path where the repository will be cloned or updated.

#     Returns:
#         Path: The local path of the cloned or updated repository.
#     """
#     local_path.parent.mkdir(parents=True, exist_ok=True)
#     # If local_path/.git exists pull, otherwise clone
#     if (local_path/".git").exists():
#         repo = Repo(local_path)
#         repo.remotes.origin.pull()
#     else:
#         print("Starting cloning...")
#         try:
#             Repo.clone_from(repo_url, local_path)
#         except Exception as e:
#             print(e)
#         print("Git clone completed")
#     return local_path  
    
from pathlib import Path
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

def load_repository(repo_url: str, local_path: Path) -> Path:
    """
    Fast-clones only 'src/oss/langgraph' if it doesn't exist locally; 
    otherwise updates it using sparse-checkout.

    Args:
        repo_url (str): The URL of the GitHub repository.
        local_path (Path): The local destination directory.

    Returns:
        Path: The local path of the repository.
    """
    target_folder = "src/oss/langgraph"
    local_path.mkdir(parents=True, exist_ok=True)
    
    # If local_path/.git exists, update it
    if (local_path / ".git").exists():
        print(f"Updating existing repository at {local_path}...")
        try:
            repo = Repo(local_path)
            repo.remotes.origin.fetch(depth=1, filter="blob:none")
            repo.git.pull()
            print("Git update completed.")
        except (GitCommandError, InvalidGitRepositoryError) as e:
            print(f"Error updating repository: {e}")
    else:
        print(f"Starting optimized fast-clone for '{target_folder}'...")
        try:
            repo = Repo.init(local_path)
            origin = repo.create_remote("origin", repo_url)
            
            #Restrict to the specific folder
            repo.git.sparse_checkout("set", target_folder)
            
            origin.fetch(depth=1, filter="blob:none")
            
            repo.git.checkout("main")
            print("Git clone completed successfully.")
            
        except (GitCommandError, InvalidGitRepositoryError) as e:
            print(f"Error cloning repository: {e}")
            
    return local_path
