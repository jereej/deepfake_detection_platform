# A collection of miscellaneous functions. Most functions are related to models or input validation.

import subprocess
from pathlib import Path
from ollama import pull, delete, ResponseError
from huggingface_hub import errors, snapshot_download, scan_cache_dir
from huggingface_hub.utils.tqdm import disable_progress_bars
from ..utils.constants import MEDIA_EXTENSIONS


def detect_backend(model: str, backend_override: str | None = None) -> str:
    """Checks if a model belongs to ollama or huggingface"""
    if backend_override:
        return backend_override
    return "huggingface" if "/" in model else "ollama"


def validate_input_argument(input: str, subfolders: bool = False, media_type: str = "image") -> list[str] | None:
    """Checks that the input argument is correct and returns list[str] for ollama"""
    extensions = MEDIA_EXTENSIONS[media_type]
    # print(f"Extensions are: {extensions}")
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
        # print(f"Subfolders is: {subfolders}")
        iterator = path.rglob("*") if subfolders else path.iterdir()
        files = [str(f) for f in sorted(iterator) if f.is_file() and f.suffix.lower() in extensions]
        if not files:
            print(
                f"No {', '.join(extensions)} files were found, please check that "
                f"the media type is correct and you have given the correct folder that the files should reside in."
            )
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


# Ollama-related functions
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


def is_ollama_model_downloaded(model: str) -> bool:
    """Checks if the model given as input is downloaded onto the machine (ollama)"""
    return model in str(subprocess.run(["ollama", "ls"], text=True, capture_output=True))


def pull_ollama_model(model: str) -> bool:
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


def list_models() -> str:
    """Lists all the models via 'ollama ls' instead of the python library equivalent"""
    return subprocess.run(["ollama", "ls"], text=True, capture_output=True).stdout


# Huggingface-related functions
def is_hf_model_downloaded(model: str) -> bool:
    """Checks if the model given as input is downloaded onto the machine (hf)"""
    cache_info = scan_cache_dir()
    return any(repo.repo_id == model for repo in cache_info.repos)


def download_hf_model(model: str) -> bool:
    download_successful = False
    try:
        with disable_progress_bars():
            snapshot_download(model)
        download_successful = True
        print(f"Model '{model}' downloaded successfully")
    except (ValueError, errors.RepositoryNotFoundError, errors.IncompleteSnapshotError) as e:
        print(f"an error occurred: {e}")
    return download_successful


def list_local_hf_models() -> str:
    """Lists locally available huggingface models"""
    return subprocess.run(["hf", "cache", "ls"], text=True, capture_output=True).stdout


def delete_hf_model(model: str) -> bool:
    """Deletes huggingface model"""
    cache_info = scan_cache_dir()
    for repo in cache_info.repos:
        if repo.repo_id == model:
            rev_hashes = [rev.commit_hash for rev in repo.revisions]
            strategy = cache_info.delete_revisions(*rev_hashes)
            strategy.execute()
            print(f"Deleted '{model}', freed {strategy.expected_freed_size_str}")
            return True
    print(f"Model '{model}' not found locally.")
    return False
