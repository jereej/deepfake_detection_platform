# A collection of miscellaneous functions. Most functions are related to models or input validation.

import subprocess
import re
from pathlib import Path
from ollama import pull, delete, ResponseError
from huggingface_hub import errors, snapshot_download, scan_cache_dir
from ..utils.constants import MEDIA_EXTENSIONS, LABELS_FILENAME
from datasets import load_dataset
import shutil
import soundfile as sf
import os
from beaupy.spinners import Spinner, DOTS


def detect_backend(model: str, backend_override: str | None = None) -> str:
    """Checks if a model belongs to ollama or huggingface"""
    if backend_override:
        return backend_override
    return "huggingface" if "/" in model else "ollama"


def validate_input_argument(arg: str, subfolders: bool = False, media_type: str = "image") -> list[str] | None:
    """Checks that the input argument is correct and returns list[str] for ollama"""
    extensions = MEDIA_EXTENSIONS[media_type]
    # If WSL in use and input file(s)/folder(s) reside under f.ex. C:/.../mnt/c/...
    # This should help mutate the input path correctly
    if re.match(r"^[a-zA-Z]:[/\\]", arg):
        drive = arg[0].lower()
        arg = arg[2:].replace("\\", "/")
        arg = f"/mnt/{drive}{arg}"
    path = Path(arg)

    if not path.exists():
        print(f"ERROR: Could not find path for {arg}")
        return None

    if path.is_file():
        if path.suffix.lower() not in extensions:
            print("ERROR: File type is incorrect. Please use the --media-type flag for text, audio or video files.")
            return None
        return [str(path)]

    if path.is_dir():
        iterator = path.rglob("*") if subfolders else path.iterdir()
        # LABELS_FILENAME is skipped: for --media-type text the .txt media
        # extension also matches the labels file, which would otherwise be fed
        # to the model as an item to analyze.
        files = [
            str(f)
            for f in sorted(iterator)
            if f.is_file() and f.suffix.lower() in extensions and f.name != LABELS_FILENAME
        ]
        if not files:
            print(
                f"No {', '.join(extensions)} files were found, please check that "
                f"the media type is correct and you have given the correct folder that the files should reside in."
            )
            return None
        return files
    print(f"ERROR: {arg} is not a valid file or folder")
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


def load_labels(path: str | Path) -> dict[str, str]:
    """Parses a labels file of 'name.ext: label' lines into a name -> raw label mapping.

    Label values are kept as strings on purpose: which value means "deepfake" is a property
    of the dataset, not of DEFTOR, so the caller states it via --positive-label. Returning
    strings also avoids silently dropping datasets whose labels are not plain 0/1.
    """
    labels: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        name, _, value = line.partition(":")
        name = name.strip()
        if name:
            labels[name] = value.strip()
    return labels


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
        spinner = Spinner(DOTS, f"Attempting to pull model '{model}'")
        spinner.start()
        pull(model)
        spinner.stop()
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
        snapshot_download(model)
        download_successful = True
        print(f"Model '{model}' downloaded successfully")
    except (ValueError, errors.RepositoryNotFoundError, errors.IncompleteSnapshotError) as e:
        print(f"an error occurred: {e}")
    return download_successful


def list_local_hf_models() -> str:
    """Lists locally available huggingface models"""
    allowed_lines = ["ID", "---", "model/"]
    cache_output = subprocess.run(
        ["hf", "cache", "ls", "--no-truncate"], text=True, capture_output=True
    ).stdout.splitlines()
    # Filtering out datasets/ and other unnecessary output
    hf_models = [line for line in cache_output if any(x in line for x in allowed_lines)]
    return "\n".join(hf_models)


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


def get_dataset(
    dataset_name: str, name_prefix: str = "item", max_items: int = 100, seed: int = 42, split: str = "train"
):
    """
    Downloads a dataset (image, audio, or video), saves media locally,
    and writes out a labels file.

    - If the dataset has <= max_items, saves all of it.
    - If larger, saves a random subset of size max_items.
    """
    dataset = load_dataset(dataset_name)

    if split not in dataset:
        split = list(dataset.keys())[0]
        print(f"Requested split not found, using '{split}' instead")

    data = dataset[split]
    total = len(data)
    print(f"Total items in '{split}' split: {total}")
    print(f"Columns: {data.column_names}")

    if total > max_items:
        print(f"Dataset larger than {max_items}, sampling a random subset...")
        data = data.shuffle(seed=seed).select(range(max_items))
    else:
        print(f"Dataset is small enough, using all {total} items.")

    n = len(data)
    pad = len(str(n))

    # --- detect media column + modality ---
    media_col, modality = None, None
    for candidate in ["image", "img"]:
        if candidate in data.column_names:
            media_col, modality = candidate, "image"
            break
    if not media_col:
        for candidate in ["audio"]:
            if candidate in data.column_names:
                media_col, modality = candidate, "audio"
                break
    if not media_col:
        for candidate in ["video", "video_path"]:
            if candidate in data.column_names:
                media_col, modality = candidate, "video"
                break

    if not media_col:
        raise ValueError(f"No recognizable media column found in {data.column_names}")

    print(f"Detected modality: {modality} (column: '{media_col}')")

    # --- detect label column ---
    label_col = None
    for candidate in ["label", "labels", "class"]:
        if candidate in data.column_names:
            label_col = candidate
            break

    ext = {"image": "png", "audio": "wav", "video": "mp4"}[modality]

    with open(f"{name_prefix}_labels.txt", "w") as f:
        for i in range(n):
            item = data[i]
            media = item[media_col]
            filename = f"{name_prefix}_{str(i + 1).zfill(pad)}.{ext}"

            if modality == "image":
                media.save(filename)

            elif modality == "audio":
                # HF audio feature gives dict: {"array": np.ndarray, "sampling_rate": int, "path": ...}
                array = media["array"]
                sr = media["sampling_rate"]
                sf.write(filename, array, sr)

            elif modality == "video":
                # HF video columns are usually a file path or decord VideoReader
                if isinstance(media, str) and os.path.exists(media):
                    shutil.copy(media, filename)
                elif isinstance(media, dict) and "path" in media:
                    shutil.copy(media["path"], filename)
                else:
                    print(f"Skipping item {i}: unrecognized video format ({type(media)})")
                    continue

            label_value = item[label_col] if label_col else "unknown"
            f.write(f"{filename}: {label_value}\n")

    print(f"Saved {n} {modality} files and labels to '{name_prefix}_labels.txt'")
    return data
