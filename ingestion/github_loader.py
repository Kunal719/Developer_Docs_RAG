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


def load_repository(repo_url: str, local_path: Path, branch: str = "main", check_for_updates: bool = True,) -> Path:
    """
    Clone or update a GitHub repository using sparse checkout.

    Only the required documentation directory is checked out to reduce
    download size and startup time.

    Args:
        repo_url: GitHub repository URL.
        local_path: Local repository directory.
        branch: Branch to checkout.
        check_for_updates: Pull latest changes if repository already exists.

    Returns:
        Path to the local repository.
    """

    target_folder = "src/oss/langgraph"

    local_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if (local_path / ".git").exists():
            repo = Repo(local_path)

            if check_for_updates:
                print("Checking for repository updates...")

                repo.remotes.origin.fetch(
                    depth=1,
                    filter="blob:none",
                )

                repo.git.pull()

                print("Repository updated successfully.")

            return local_path

        print("Cloning documentation repository...")

        repo = Repo.clone_from(
            repo_url,
            local_path,
            branch=branch,
            depth=1,
            filter="blob:none",
            no_checkout=True,
        )

        repo.git.sparse_checkout("init", "--cone")
        repo.git.sparse_checkout("set", target_folder)

        repo.git.checkout(branch)

        print("Repository cloned successfully.")

        return local_path

    except (GitCommandError, InvalidGitRepositoryError) as exc:
        raise RuntimeError(
            f"Failed to prepare repository: {exc}"
        ) from exc