# This file contains logic related to outputting the already formatted LLM results in an user-specified manner
import json
import csv
import yaml
from pathlib import Path
from .prompter import ResponseObject

DEFAULT_OUTPUT_DIR = Path.cwd() / "analyses"


def write_output_file(
    output_filename: str,
    analysis_result: list[ResponseObject] | None,
    extension: str,
    destination: str,
) -> bool:
    if not analysis_result:
        return False
    try:
        dest_dir = Path(destination) if destination else DEFAULT_OUTPUT_DIR
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / f"{output_filename}"

        contents = [res.model_dump() for res in analysis_result]

        if extension == "json":
            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump({"result": contents}, f, indent=2)

        elif extension in ("yaml", "yml"):
            with open(dest_path, "w", encoding="utf-8") as f:
                yaml.safe_dump({"result": contents}, f)

        elif extension == "csv":
            with open(dest_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["image_name", "classification", "confidence_score", "evidence"])
                for row in contents:
                    writer.writerow(
                        [
                            row["image_name"],
                            row["classification"],
                            "; ".join(row["evidence"]),
                        ]
                    )
        else:
            with open(dest_path, "w", encoding="utf-8") as f:
                for entry in contents:
                    f.write(
                        f"Image name: {entry['image_name']}\n"
                        f"Classification: {entry['classification']}\n"
                        f"Evidence: {'\n          '.join(entry['evidence'])}\n\n"
                    )

        print(f"Output has been written to {dest_path}")
        return True
    except OSError as e:
        print(f"An error occurred: {e}")
    return False


def write_output_to_stdout(analysis_result: list[ResponseObject], as_text: bool = True) -> bool:
    if not analysis_result:
        print("Analysis result was not provided, exiting...")
        return False

    contents = [res.model_dump() for res in analysis_result]
    if as_text:
        for entry in contents:
            print(
                f"\nImage name: {entry['image_name']}\n"
                f"Classification: {entry['classification']}\n"
                f"Evidence: {'\n          '.join(entry['evidence'])}\n"
            )
    else:
        print(f"{contents}")
    return True
