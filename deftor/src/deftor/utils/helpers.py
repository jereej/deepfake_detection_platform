# Any function that is setup/system/file related

import json
import subprocess
from importlib import resources
from pathlib import Path
from ollama import pull, delete, ResponseError


# Misc functions
def load_data(file_name: str) -> dict:
    """Reads data from given .json file under src/deftor/utils"""
    data = resources.files("deftor.utils").joinpath(file_name).read_text(encoding="utf-8")
    return json.loads(data)


def validate_input_argument(input: str) -> list[str] | None:
    """Checks that the input argument is correct and returns list[str] for ollama"""
    extensions = {".jpg", ".jpeg", ".png"}  # Can be extended if required
    path = Path(input)

    if not path.exists():
        print(f"ERROR: Could not find path for {input}")
        return None

    if path.is_file():
        if path.suffix.lower() not in extensions:
            print(f"ERROR: File type for '{input}' has to be .jpg, .jpeg or .png")
            return None
        return [str(path)]

    if path.is_dir():
        files = [str(f) for f in sorted(path.iterdir()) if f.is_file() and f.suffix.lower() in extensions]
        if not files:
            print(f"No .jpg or .png files found for {input}")
            return None
        return files
    print(f"ERROR: {input} is not a valid file or folder")
    return None


def validate_output_argument(output: str) -> bool:
    """Check that user does not give file extensions to the output argument"""
    suffix = Path(output).suffix
    if suffix:
        print(
            f"Output argument should not include file extensions ({suffix})."
            f"Please use the -f/--format argument to specify extensions."
        )
        return False
    return True


# Ollama related functions
def is_ollama_installed() -> bool:
    """Checks if ollama is installed on the machine"""
    return (
        subprocess.run(
            ["ollama", "-v"],
            shell=False,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


def is_model_downloaded(model: str) -> bool:
    """Checks if the model given as input is downloaded onto the machine"""
    return model in str(subprocess.run(["ollama", "ls"], text=True, capture_output=True))


def pull_model(model: str) -> bool:
    """Attempts to pull the given ollama model"""
    pull_successful = False
    try:
        print(f"Attempting to pull model '{model}'")
        pull(model)
        pull_successful = True
        print(f"Pulled model '{model}' successfully.")
    except ResponseError as e:
        if e.status_code == 500:
            print(f"Model '{model}' could not be pulled. Please check that the model name is correct.")
            print("You can find a list of available models at https://ollama.com/search")
        else:
            print(f"An error occurred: {e}")
    return pull_successful


def delete_model(model: str) -> bool:
    """Attempts to delete the given ollama model"""
    delete_successful = False
    try:
        delete(model)
        delete_successful = True
        print(f"Deleted model '{model}' successfully.")
    except ResponseError as e:
        if e.status_code == 404:
            print(f"Could not find model '{model}' to delete.")
        else:
            print(f"An error occurred: {e}")
    return delete_successful


def list_models() -> None:
    """Lists all the models via 'ollama ls' instead of the python library equivalent"""
    print(subprocess.run(["ollama", "ls"], text=True, capture_output=True).stdout)
