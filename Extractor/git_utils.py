import subprocess
import os

def run_git_command(command, cwd=None):
    # Execute a Git command and capture its output
    try:
        result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Raise an exception with the error message if the command fails
        raise Exception(f"Git command failed: {e.stderr}")

def clone_or_update_repo(repo_url, branch, local_repo_dir):
    # Clone the repository if it doesn't exist, otherwise update it
    # Currently not used, as Localization is in the repository root
    if not os.path.exists(local_repo_dir):
        print(f"Cloning repository from {repo_url} to {local_repo_dir}")
        run_git_command(["git", "clone", "--branch", branch, repo_url, local_repo_dir])
    else:
        print(f"Updating repository in {local_repo_dir}")
        # Fetch the latest changes from the remote repository
        run_git_command(["git", "fetch", "origin"], cwd=local_repo_dir)
        # Checkout the specified branch
        run_git_command(["git", "checkout", branch], cwd=local_repo_dir)
        # Pull the latest changes
        run_git_command(["git", "pull", "origin", branch], cwd=local_repo_dir)
    print("Repository is up to date")
