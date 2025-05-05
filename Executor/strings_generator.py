#!/usr/bin/env python3

# Standard library imports for file handling, arguments, and path manipulation
import os
import sys
import argparse
import subprocess
import shutil

# Check for PyYAML dependency
try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Please install it using:")
    print("  pip install pyyaml")
    exit(1)

def run_git_command(command, cwd=None):
    # Execute a Git command and capture its output
    try:
        result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git command failed: {e.stderr}")

def clone_or_update_repo(repo_url, branch, local_repo_dir):
    # Clone or update the localization repository
    if not os.path.exists(local_repo_dir):
        print(f"Cloning repository from {repo_url} to {local_repo_dir}")
        run_git_command(["git", "clone", "--branch", branch, repo_url, local_repo_dir])
    else:
        print(f"Updating repository in {local_repo_dir}")
        run_git_command(["git", "fetch", "origin"], cwd=local_repo_dir)
        run_git_command(["git", "checkout", branch], cwd=local_repo_dir)
        run_git_command(["git", "pull", "origin", branch], cwd=local_repo_dir)
    print("Repository is up to date")

def cleanup(local_repo_dir):
    # Remove the temporary repository directory if it exists
    if os.path.exists(local_repo_dir):
        try:
            shutil.rmtree(local_repo_dir)
            print(f"Successfully removed {local_repo_dir}")
        except Exception as e:
            print(f"Failed to remove {local_repo_dir}: {e}")
    else:
        print(f"No directory to remove: {local_repo_dir}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate localization files for multiple platforms")
    parser.add_argument("--platform", choices=["ios", "android", "web", "all"], default="ios",
                        help="Target platform for localization (only iOS supported for now)")
    args = parser.parse_args()

    # Define paths
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_url = "https://github.com/artembilyy/PolisUA-localization"
    branch = "main"
    local_repo_dir = os.path.join(script_dir, "repo")

    try:
        # Clone or update the localization repository
        clone_or_update_repo(repo_url, branch, local_repo_dir)

        # Add the cloned repository to sys.path to import modules
        sys.path.insert(0, local_repo_dir)

        # Import modules from the cloned repository
        from config import Config
        from Extractor.yaml_parser import collect_yaml_data
        from Extractor.generators.ios_generator import generate_ios
        from Extractor.generators.android_generator import generate_android
        from Extractor.generators.web_generator import generate_web

        # Initialize configuration
        config = Config()
        
        # Collect and parse YAML localization data
        all_tables = collect_yaml_data(config.yaml_dir)

        # Generate localization files based on the specified platform
        if args.platform in ["ios", "all"]:
            generate_ios(all_tables, config.ios_output_dir, config.ios_enum_output)
        if args.platform in ["android", "all"]:
            generate_android(all_tables, config.android_output_dir)
        if args.platform in ["web", "all"]:
            generate_web(all_tables, config.web_output_dir)

        print("Localization: Success")
    except Exception as e:
        print(f"Failed to process localization: {e}")
        exit(1)
    finally:
        # Always attempt to clean up and remove repo from sys.path
        cleanup(local_repo_dir)
        if local_repo_dir in sys.path:
            sys.path.remove(local_repo_dir)

if __name__ == "__main__":
    main()
