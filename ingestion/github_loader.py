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
from enum import Enum

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

class RepositoryStatus(Enum):
    """
    Status of repository after syncing the local repo from the remote repo
    """
    CLONED = "cloned"
    UPDATED = "updated"
    UNCHANGED = "unchanged"

def load_repository(repo_url: str, local_path: Path, branch: str = "main", check_for_updates: bool = True,) -> tuple[Path, RepositoryStatus]:
    """
    Clone or update a GitHub repository using sparse checkout.

    Only the required documentation directory is checked out to reduce
    download size and startup time.

    The local repository is treated as a read-only mirror of the upstream
    documentation. Updates are synchronized by resetting to the latest remote
    commit instead of merging local history.

    Args:
        repo_url: GitHub repository URL.
        local_path: Local repository directory.
        branch: Branch to checkout.
        check_for_updates: Pull latest changes if repository already exists.

    Returns:
        A tuple containing the local repository path and the repository status.
    """

    target_folder = "src/oss/langgraph"

    local_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if (local_path / ".git").exists():
            repo = Repo(local_path)

            if not check_for_updates:
                return local_path, RepositoryStatus.UNCHANGED

            print("Checking for repository updates...")

            repo.remotes.origin.fetch(
                depth=1,
                filter="blob:none",
            )

            local_commit = repo.head.commit
            remote_commit = repo.refs[f"origin/{branch}"].commit

            # TODO:
            # Instead of comparing repository commits, compare only the tracked
            # documentation directory against origin/<branch>. This would avoid
            # pulling the repository when unrelated files outside the sparse
            # checkout path have changed.

            if local_commit.hexsha == remote_commit.hexsha:
                print("Repository is already up to date.")
                return local_path, RepositoryStatus.UNCHANGED

            # This repository is treated as a read-only mirror of the upstream
            # documentation. Rather than merging histories with `git pull`, we
            # simply make the local checkout identical to origin/<branch>.
            repo.git.reset("--hard", f"origin/{branch}")

            print("Repository updated successfully.")

            return local_path, RepositoryStatus.UPDATED

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

        return local_path, RepositoryStatus.CLONED

    except (GitCommandError, InvalidGitRepositoryError) as exc:
        raise RuntimeError(
            f"Failed to prepare repository: {exc}"
        ) from exc