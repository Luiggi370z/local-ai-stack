import os

import yaml

from utils import clone_or_update_repo, run_command

LITELLM_DOCKER_FILE_ARGS = ["-f", "litellm/docker-compose.yml"]


def clone_litellm_repo() -> None:
    """Clone the LiteLLM repository if not already present."""
    clone_or_update_repo(
        package_name="LiteLLM",
        target_folder="litellm",
        repo_url="https://github.com/BerriAI/litellm",
        branch="main",
    )


def prepare_litellm_env() -> None:
    if os.path.exists("litellm"):
        """Create .env in litellm folder and update docker-compose.yml port and db service name."""
        os.chdir("litellm")
        print("Creating .env in litellm folder...")

        with open(".env", "w") as env_file:
            env_file.write(f'LITELLM_MASTER_KEY="{os.environ["LITELLM_MASTER_KEY"]}"\n')
            env_file.write(f'LITELLM_SALT_KEY="{os.environ["LITELLM_SALT_KEY"]}"\n')

        os.chdir("..")
        print("LiteLLM env file created successfully.")


def update_litellm_docker_compose() -> None:
    """Update the LiteLLM docker-compose.yml file."""
    with open("litellm/docker-compose.yml", "r") as file:
        compose_config = yaml.safe_load(file)

    new_port = os.environ["LITELLM_PORT"]
    if new_port and new_port != "4000":
        compose_config["services"]["litellm"]["ports"] = [f"{new_port}:4000"]

    # Update database service name and references
    if "db" in compose_config["services"]:
        compose_config["services"]["db_litellm"] = compose_config["services"].pop("db")
        for service in compose_config["services"].values():
            if "depends_on" in service and "db" in service["depends_on"]:
                service["depends_on"].remove("db")
                service["depends_on"].append("db_litellm")

            if "environment" in service and "DATABASE_URL" in service["environment"]:
                service["environment"]["DATABASE_URL"] = service["environment"][
                    "DATABASE_URL"
                ].replace("db:", "db_litellm:")

    with open("litellm/docker-compose.yml", "w") as file:
        yaml.safe_dump(compose_config, file, default_flow_style=False)

    print("LiteLLM docker-compose.yml updated successfully.")


def start_litellm() -> None:
    """Start the LiteLLM services (using its compose file)."""
    print("Starting LiteLLM services...")
    run_command(
        [
            "docker",
            "compose",
            "-p",
            "localai",
            "-f",
            "litellm/docker-compose.yml",
            "up",
            "-d",
        ]
    )
