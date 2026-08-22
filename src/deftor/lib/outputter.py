# This file contains logic related to outputting the already formatted LLM results in an user-specified manner
import json
import csv
import yaml
from pathlib import Path
from .prompter import ResponseObject, HFResponseObject, RunStatistics

DEFAULT_OUTPUT_DIR = Path.cwd() / "analyses"
STATISTIC_LOG_PATH = Path.cwd() / "statistics.csv"

STATISTIC_LOG_FIELDS = [
    # Run statistic fields
    "timestamp",
    "backend",
    "model",
    "media_type",
    "number_of_items",
    "total_execution_time",
    "model_loading_time",
    # Item statistic fields
    "file_name",
    "file_size_in_bytes",
    "execution_time",
    "success",
    "error",
]


def write_analysis_output(
    output_filename: str,
    analysis_result: list[ResponseObject] | list[HFResponseObject] | None,
    stats_result: RunStatistics | None,
    extension: str,
    destination: str,
) -> bool:
    if not analysis_result:
        return False
    try:
        dest_dir = Path(destination) if destination else DEFAULT_OUTPUT_DIR
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / f"{output_filename}"

        contents = [normalize_responses(res.model_dump()) for res in analysis_result]

        if extension == "json":
            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump({"result": contents}, f, indent=2)

        elif extension in ("yaml", "yml"):
            with open(dest_path, "w", encoding="utf-8") as f:
                yaml.safe_dump({"result": contents}, f)

        elif extension == "csv":
            with open(dest_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "classification", "confidence", "evidence", "raw_label"])
                for row in contents:
                    writer.writerow(
                        [
                            row["name"],
                            row["classification"],
                            row["confidence"] if row["confidence"] is not None else "",
                            "; ".join(row["evidence"]) if row["evidence"] else "",
                            row["raw_label"] or "",
                        ]
                    )
        else:
            with open(dest_path, "w", encoding="utf-8") as f:
                write_string = []
                for entry in contents:
                    write_string.append(format_text_response(entry))
                f.write("\n".join(write_string))

        print(f"Output has been written to {dest_path}")
        if stats_result:
            append_execution_stats(stats_result)
        return True
    except OSError as e:
        print(f"An error occurred: {e}")
    return False


def normalize_responses(entry: dict) -> dict:
    return {
        "name": entry.get("image_name") or entry.get("media_name", "unknown"),
        "classification": entry.get("classification", "UNKNOWN"),
        "evidence": entry.get("evidence"),  # ollama
        "confidence": entry.get("confidence"),  # huggingface
        "raw_label": entry.get("raw_label"),  # huggingface
        "media_type": entry.get("media_type"),  # huggingface
    }


def format_text_response(response: dict) -> str:
    lines = [f"Name: {response['name']}", f"Classification: {response['classification']}"]
    if response["evidence"]:
        lines.append(f"Evidence: {response['evidence']}")
    if response["confidence"] is not None:
        lines.append(f"Confidence: {response['confidence']:.2%}")
    if response["raw_label"]:
        lines.append(f"Raw label: {response['raw_label']}")
    return "\n".join(lines) + "\n"


def write_output_to_stdout(analysis_result: list[ResponseObject], as_text: bool = True) -> bool:
    if not analysis_result:
        print("Analysis result was not provided, exiting...")
        return False

    contents = [normalize_responses(res.model_dump()) for res in analysis_result]
    if as_text:
        for entry in contents:
            print("\n" + format_text_response(entry))
    else:
        print(f"{contents}")
    return True


def append_execution_stats(stats: RunStatistics) -> bool:
    try:
        STATISTIC_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        file_exists = STATISTIC_LOG_PATH.exists()
        with open(STATISTIC_LOG_PATH, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=STATISTIC_LOG_FIELDS)
            if not file_exists:
                writer.writeheader()

            for item in stats.items:
                writer.writerow(
                    {
                        "timestamp": stats.timestamp,
                        "backend": stats.backend,
                        "model": stats.model,
                        "media_type": stats.media_type or "",
                        "number_of_items": stats.number_of_items,
                        "total_execution_time": stats.total_execution_time,
                        "model_loading_time": stats.model_loading_time or "",
                        "file_name": item.file_name,
                        "file_size_in_bytes": item.file_size_in_bytes,
                        "execution_time": item.execution_time,
                        "success": item.success,
                        "error": item.error or "",
                    }
                )
        return True
    except OSError as e:
        print(e)
        return False
