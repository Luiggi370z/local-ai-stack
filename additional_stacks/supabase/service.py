import os
import shutil

from utils import clone_or_update_repo, run_command

SUPABASE_DOCKER_FILE_ARGS = ["-f", "supabase/docker/docker-compose.yml"]


def clone_supabase_repo() -> None:
    """Clone the Supabase repository if not already present."""
    clone_or_update_repo(
        package_name="Supabase",
        target_folder="supabase",
        repo_url="https://github.com/supabase/supabase.git",
        branch="master",
    )


def prepare_supabase_env() -> None:
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")
    print("Copying .env in root to .env in supabase/docker...")
    shutil.copyfile(env_example_path, env_path)


def start_supabase() -> None:
    """Start the Supabase services (using its compose file)."""
    print("Starting Supabase services...")
    run_command(
        [
            "docker",
            "compose",
            "-p",
            "localai",
            "-f",
            "supabase/docker/docker-compose.yml",
            "up",
            "-d",
        ]
    )
