import os
import subprocess
from typing import List, Optional


def run_command(cmd: str | List[str], cwd: Optional[str] = None) -> None:
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd) if isinstance(cmd, list) else cmd)
    subprocess.run(cmd, cwd=cwd, check=True)


def clone_or_update_repo(
    package_name: str, target_folder: str, repo_url: str, branch: str = "main"
) -> None:
    """Clone or update a repository using sparse checkout.

    Args:
        package_name: Name of the package for logging
        target_folder: Folder name where to clone/update the repository
        repo_url: Git repository URL
        branch: Branch name to checkout (default: main)
    """
    if not os.path.exists(target_folder):
        print(f"Cloning the {package_name} repository...")
        run_command(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                repo_url,
            ]
        )
        os.chdir(target_folder)
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", branch])
        os.chdir("..")
    else:
        print(f"{package_name} repository already exists, updating...")
        os.chdir(target_folder)
        run_command(["git", "pull"])
        os.chdir("..")
