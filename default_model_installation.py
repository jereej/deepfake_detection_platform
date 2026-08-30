# The contents of this file deal with installing default models through DEFTOR
# Used only in installation_linux.sh but can be run separately
# f.ex. with 'uv run default_model_installation.py'
from beaupy import select_multiple, confirm
from beaupy.spinners import Spinner, DOTS
from rich.console import Console
import shutil
from pathlib import Path
from src.deftor.utils.constants import DEFAULT_MODELS
from src.deftor.utils.helpers import download_hf_model, pull_ollama_model


def format_default_models() -> list:
    """Formats the DEFAULT_MODELS into a more usable format"""
    model_list = []
    for model in DEFAULT_MODELS:
        model_list.append(f"{model['name']} ({model['info']['input']}) {model['info']['size']:.2f}GB")
    return model_list


def calculate_total_download_size(selection: list) -> float:
    """Calculates the total size of the download after selecting the models"""
    total_size = 0.0
    for item in selection:
        for model in DEFAULT_MODELS:
            if model["name"] in item:
                total_size += model["info"]["size"]
    return total_size


def download_models(selection: list) -> None:
    """Downloads selected models"""
    for item in selection:
        for model in DEFAULT_MODELS:
            if model["name"] in item:
                if model["info"]["backend"] == "ollama":
                    pull_ollama_model(model["name"])
                elif model["info"]["backend"] == "huggingface":
                    download_hf_model(model["name"])


def main() -> None:
    """The place where previous methods are used"""
    console = Console()
    download_prompt = confirm("Would you like to download some default models?")
    if not download_prompt:
        console.print("Skipping downloading default models.")
        return
    _, _, free = shutil.disk_usage(Path.cwd())
    free = free / (1024**3)
    console.print("Choose the models to download")
    selection = select_multiple(format_default_models())
    if selection:
        download_size = calculate_total_download_size(selection)
        if download_size < free:
            confirmation = confirm(
                f"The models require {download_size:.2f}GB of space "
                f"(Free space: {free:.2f}GB), are you sure you want to proceed?"
            )
            if confirmation:
                spinner = Spinner(DOTS, "Downloading models...")
                spinner.start()
                download_models(selection)
                spinner.stop()
                return
            console.print("Did not download any models.")
            return
        elif download_size > free:
            console.print(
                f"Not enough space left in the device for the download."
                f"(download size: {download_size:.2f}GB, free space on disk: {free / 1024**3:2f}GB)"
            )
    console.print("Did not choose any models to download.")
    return


main()
