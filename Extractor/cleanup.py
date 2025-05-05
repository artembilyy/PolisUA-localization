import shutil
import os

def cleanup(local_repo_dir):
    # Remove the temporary repository directory if it exists
    if os.path.exists(local_repo_dir):
        shutil.rmtree(local_repo_dir)
        print(f"Removed {local_repo_dir}")
