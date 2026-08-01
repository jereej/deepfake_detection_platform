# CLI for the deepfake detection platform (DEFTOR)

import argparse
from datetime import datetime
from .lib.outputter import write_output_file, write_output_to_stdout
from .utils.helpers import (
    is_ollama_installed,
    is_model_downloaded,
    pull_model,
    delete_model,
    validate_input_argument,
    validate_output_argument,
    list_models,
)
from .lib.prompter import image_prompt_ollama


def run_cli() -> None:
    # Instantly return if ollama is not installed
    if not is_ollama_installed():
        print(
            "Ollama is required but was not found on this system.\n"
            "Please download it from https://ollama.com/download, and then re-run this command."
        )
        return

    parser = argparse.ArgumentParser(prog="deftor")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analyzer subcommands
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze images for signs of AI manipulation using a local Ollama vision model.",
    )
    analyze_parser.add_argument("input", type=str, help="Path to an image or a folder or images")
    analyze_parser.add_argument(
        "-m",
        "--model",
        type=str,
        required=True,
        help="Name of the used model (f.ex. llava or llava:latest)",
    )
    analyze_parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="Output filename without file extension. Without this parameter, output is directed to stdout. Also includes a timestamp in the YYYYMMDDHHMMSS format",
    )
    analyze_parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["json", "yaml", "yml", "csv", "txt"],
        help="Output format (default is txt)",
    )
    analyze_parser.add_argument("-t", "--target", type=str, required=False, help="Target folder of the analysis")

    analyze_parser.add_argument(
        "--no-timestamp",
        action="store_false",
        help="Used with -o, if you want to write the file name without the timestamp",
    )
    analyze_parser.add_argument(
        "--raw",
        action="store_false",
        help="If you want the raw LLM analysis output piped to stdout",
    )

    # Model subcommands
    model_parser = subparsers.add_parser("model", help="Manage local Ollama models (pull, delete, list)")
    model_subparsers = model_parser.add_subparsers(dest="model_command", required=True)
    pull_parser = model_subparsers.add_parser("pull", help="Download a model from Ollama's library ")
    pull_parser.add_argument("name", type=str, help="Name of the model to pull (e.g. llava)")
    delete_parser = model_subparsers.add_parser("delete", help="Delete a model from the local system")
    delete_parser.add_argument("name", type=str, help="Name of the model to delete (e.g. llava)")
    model_subparsers.add_parser("list", help="List all locally available models")

    args = parser.parse_args()
    # Logic block for arguments

    if args.command == "analyze":
        images = validate_input_argument(args.input)
        if not images:
            return
        if not is_model_downloaded(args.model):
            print(f"Could not find model '{args.model}'. Attempting to pull it.")
            if not pull_model(args.model):
                return
        if args.format and not args.output:
            print("-f given without -o, please specify a filename to write output into a file. Outputting into stdout")
            return
        if args.output:
            if not validate_output_argument(args.output):
                return
        # MAIN FUNCTION
        ai_analysis_result = image_prompt_ollama(model=args.model, image_paths=images)
        # AFTER WHICH SPECIFY HOW TO OUTPUT RESULTS
        if ai_analysis_result:
            if args.output:
                fmt = ""
                if not args.format:
                    fmt = "txt"
                timestamp = ""
                if args.no_timestamp:
                    timestamp = f"_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                output_filename = f"{args.output}{timestamp}.{args.format or fmt}"
                # print(f"DEBUG: output_filename is: {output_filename}")
                write_output_file(
                    output_filename=output_filename,
                    analysis_result=ai_analysis_result,
                    extension=args.format,
                    destination=args.target,
                )
                return
            else:
                write_output_to_stdout(ai_analysis_result, args.raw)
    if args.command == "model":
        if args.model_command == "pull":
            pull_model(args.name)
        if args.model_command == "delete":
            delete_model(args.name)
        if args.model_command == "list":
            list_models()
