# CLI for the deepfake detection platform (DEFTOR)

import argparse
from datetime import datetime
from .lib.outputter import write_analysis_output, write_output_to_stdout
from .utils.helpers import (
    is_ollama_model_downloaded,
    pull_ollama_model,
    delete_model,
    validate_input_argument,
    validate_output_argument,
    list_models,
    detect_backend,
    is_hf_model_downloaded,
    download_hf_model,
    list_local_hf_models,
    delete_hf_model,
)
from .lib.prompter import prompt_model
from .lib.reporter import create_report
import json


def run_cli() -> None:

    parser = argparse.ArgumentParser(prog="deftor")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analyzer subcommands
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze images for signs of AI manipulation using a local Ollama vision model.",
    )
    analyze_parser.add_argument("input", type=str.strip, help="Path to an image or a folder or images")
    analyze_parser.add_argument(
        "-m",
        "--model",
        type=str.strip,
        required=True,
        help="Name of the used model (f.ex. llava or llava:latest)",
    )
    analyze_parser.add_argument(
        "-o",
        "--output",
        type=str.strip,
        required=False,
        help="Output filename without file extension. Without this parameter, output is directed to stdout."
        "Also includes a timestamp in the YYYYMMDDHHMMSS format",
    )
    analyze_parser.add_argument(
        "-f",
        "--format",
        type=str.strip,
        choices=["json", "yaml", "yml", "csv", "txt"],
        help="Output format (default is txt)",
    )
    analyze_parser.add_argument(
        "-d", "--destination", type=str.strip, required=False, help="Destination folder of the analysis"
    )

    analyze_parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Used with -o, if you want to write the file name without the timestamp",
    )
    analyze_parser.add_argument(
        "--raw",
        action="store_false",
        help="If you want the raw LLM analysis output piped to stdout",
    )

    analyze_parser.add_argument(
        "--subfolders",
        action="store_true",
        help="Give this argument if you want to analyze all images under given folder's subfolders "
        "(e.g. input=/path/images and images contains images/folder1 and images/folder2)",
    )

    analyze_parser.add_argument(
        "--model-options",
        type=json.loads,
        required=False,
        help='Options to give the model (ollama). Give them in the following format: \'{"option": "value", "option2": 1}\'.'
        " Options are typically model-specific so please look at Ollama's website for the supported values.",
    )

    analyze_parser.add_argument(
        "--backend",
        type=str.strip,
        choices=["ollama", "huggingface"],
        required=False,
        help="Force the model backend through this argument. Usually it is automatically detected"
        " from the model name (e.g. 'llava' or 'llava:latest' -> ollama, 'user/model-name' -> huggingface)"
        ". Some HF models might not use / and that is when this argument should be given. Some Ollama "
        "models also support / in the name so it works there as well.",
    )

    analyze_parser.add_argument(
        "--media-type",
        type=str.strip,
        choices=["text", "image", "audio", "video"],
        required=False,
        default="image",
        help="Type of media to be analyzed, either text, image, audio or video. Image by default",
    )

    # Model subcommands
    model_parser = subparsers.add_parser("model", help="Manage local models (pull, delete, list)")
    model_subparsers = model_parser.add_subparsers(dest="model_command", required=True)
    pull_parser = model_subparsers.add_parser("pull", help="Download a model.")
    pull_parser.add_argument("name", type=str.strip, help="Name of the model to pull (e.g. llava)")
    delete_parser = model_subparsers.add_parser("delete", help="Delete a model from the local system")
    delete_parser.add_argument("name", type=str.strip, help="Name of the model to delete (e.g. llava)")
    model_subparsers.add_parser("list", help="List all locally available models")

    # Ollama also supports users to upload their own models so these overrides are required here as well.
    pull_parser.add_argument(
        "--backend",
        type=str.strip,
        choices=["ollama", "huggingface"],
        required=False,
        help="Force the model backend through this argument. Usually it is automatically detected"
        " from the model name (e.g. 'llava' or 'llava:latest' -> ollama, 'user/model-name' -> huggingface)"
        ". Some HF models might not use / and that is when this argument should be givenSome Ollama "
        "models also support / in the name so it works there as well.",
    )

    delete_parser.add_argument(
        "--backend",
        type=str.strip,
        choices=["ollama", "huggingface"],
        required=False,
        help="Force the model backend through this argument. Usually it is automatically detected"
        " from the model name (e.g. 'llava' or 'llava:latest' -> ollama, 'user/model-name' -> huggingface)"
        ". Some HF models might not use / and that is when this argument should be given. Some Ollama "
        "models also support / in the name so it works there as well.",
    )

    # Reporter stuff
    subparsers.add_parser(
        "report",
        help="Create a report based on statistics.csv",
    )

    args = parser.parse_args()
    # Logic block for arguments
    if args.command == "analyze":
        images = validate_input_argument(args.input, args.subfolders, args.media_type)
        if not images:
            return
        # DEFTOR supports both ollama and huggingface equally, so both are handled here.
        # This means that ALL LOGIC needs to be handled in parallel
        backend = detect_backend(args.model, args.backend)
        if backend == "ollama":
            if not is_ollama_model_downloaded(args.model):
                print(f"Could not find model '{args.model}'. Attempting to pull it.")
                if not pull_ollama_model(args.model):
                    return
        elif backend == "huggingface":
            if not is_hf_model_downloaded(args.model):
                print(f"Could not find model '{args.model}'. Attempting to pull it.")
                if not download_hf_model(args.model):
                    return
        if args.format and not args.output:
            print("-f given without -o, please specify a filename to write output into a file. Outputting into stdout")
            return
        if args.output:
            if not validate_output_argument(args.output):
                return
        # MAIN FUNCTION
        ai_analysis_result, stats_result = prompt_model(
            backend, model=args.model, image_paths=images, options=args.model_options
        )
        # AFTER WHICH SPECIFY HOW TO OUTPUT RESULTS
        if ai_analysis_result:
            if args.output:
                fmt = ""
                if not args.format:
                    fmt = "txt"
                timestamp = f"_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                if args.no_timestamp:
                    timestamp = ""
                output_filename = f"{args.output}{timestamp}.{args.format or fmt}"
                write_analysis_output(
                    output_filename=output_filename,
                    stats_result=stats_result,
                    analysis_result=ai_analysis_result,
                    extension=args.format,
                    destination=args.destination,
                )
                return
            else:
                write_output_to_stdout(ai_analysis_result, args.raw)
    if args.command == "model":
        if args.model_command == "list":
            ollama_models = list_models()
            hf_models = list_local_hf_models()
            print(f"Ollama models:\n{ollama_models}")
            print(f"Huggingface models:\n{hf_models}")
            return
        backend = detect_backend(args.name, args.backend)
        if args.model_command == "pull":
            if backend == "ollama":
                pull_ollama_model(args.name)
            elif backend == "huggingface":
                download_hf_model(args.name)
        if args.model_command == "delete":
            if backend == "ollama":
                delete_model(args.name)
            elif backend == "huggingface":
                delete_hf_model(args.name)
    if args.command == "report":
        create_report()
