# This file contains logic related to outputting the already formatted LLM results in an user-specified manner
import json
import csv
import yaml
from pathlib import Path
from .prompter import ResponseObject, HFResponseObject, RunStatistics
from ..utils.constants import DEFAULT_OUTPUT_DIR, STATISTIC_LOG_FIELDS, STATISTIC_LOG_FILENAME, STATISTIC_LOG_PATH


# Per-item fields, in output order, for the flat CSV variant
ITEM_CSV_FIELDS = [
    "name",
    "classification",
    "fake_score",
    "confidence",
    "raw_label",
    "media_type",
    "label",
    "file_size_in_bytes",
    "execution_time",
    "success",
    "finish_reason",
    "error",
]

# Run-level fields embedded in the analysis file
RUN_FIELDS = [
    "run_id",
    "timestamp",
    "backend",
    "model",
    "media_type",
    "dataset",
    "labels_file",
    "positive_label",
    "number_of_items",
    "number_succeeded",
    "number_failed",
    "total_execution_time",
    "model_loading_time",
    "total_duration_ns",
    "load_duration_ns",
    "prompt_eval_count",
    "eval_count",
    "eval_duration_ns",
]


def resolve_destination(destination: str | None) -> Path:
    return Path(destination) if destination else DEFAULT_OUTPUT_DIR


def resolve_statistics_path(destination: str | None) -> Path:
    """Statistics live next to the analysis files so -d keeps everything together."""
    if destination:
        return Path(destination) / STATISTIC_LOG_FILENAME
    return STATISTIC_LOG_PATH


def build_run_block(stats: RunStatistics) -> dict:
    """Run-level metadata embedded in the analysis file.

    Embedding this makes each analysis file self-contained, so metrics never depend on
    parsing the filename or joining against statistics.csv.
    """
    succeeded = sum(1 for item in stats.items if item.success)
    block = {field: getattr(stats, field, None) for field in RUN_FIELDS}
    block["number_succeeded"] = succeeded
    block["number_failed"] = len(stats.items) - succeeded
    return block


def normalize_responses(entry: dict) -> dict:
    return {
        "name": entry.get("image_name") or entry.get("media_name", "unknown"),
        "classification": entry.get("classification", "UNKNOWN"),
        "evidence": entry.get("evidence"),  # ollama
        "confidence": entry.get("confidence"),  # huggingface
        "fake_score": entry.get("fake_score"),  # huggingface, P(DEEPFAKE)
        "raw_label": entry.get("raw_label"),  # huggingface
        "media_type": entry.get("media_type"),  # huggingface
    }


def build_item_records(
    analysis_result: list[ResponseObject] | list[HFResponseObject] | None,
    stats_result: RunStatistics | None,
    labels: dict[str, str] | None = None,
) -> list[dict]:
    """Merges predictions with per-item execution statistics into one flat record list.

    Iterating the statistics rather than the predictions is deliberate: items that failed to
    validate or errored never reach `analysis_result`, but they are exactly the ones worth
    keeping in the output (with their error and timing).
    """
    predictions: dict[str, dict] = {}
    for response in analysis_result or []:
        normalized = normalize_responses(response.model_dump())
        predictions[normalized["name"]] = normalized

    def record(name: str, prediction: dict | None, item=None) -> dict:
        prediction = prediction or {}
        return {
            "name": name,
            "classification": prediction.get("classification"),
            "fake_score": prediction.get("fake_score"),
            "confidence": prediction.get("confidence"),
            "raw_label": prediction.get("raw_label"),
            "media_type": prediction.get("media_type") or (stats_result.media_type if stats_result else None),
            "evidence": prediction.get("evidence"),
            "label": labels.get(name) if labels else None,
            "file_size_in_bytes": item.file_size_in_bytes if item else None,
            "execution_time": item.execution_time if item else None,
            "success": item.success if item else None,
            "finish_reason": item.finish_reason if item else None,
            "error": item.error if item else None,
        }

    records: list[dict] = []
    seen: set[str] = set()
    if stats_result:
        for item in stats_result.items:
            seen.add(item.file_name)
            records.append(record(item.file_name, predictions.get(item.file_name), item))
    # Defensive: keep any prediction that has no matching statistics row.
    for name, prediction in predictions.items():
        if name not in seen:
            records.append(record(name, prediction))
    return records


def _csv_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    return str(value)


def write_analysis_output(
    output_filename: str,
    analysis_result: list[ResponseObject] | list[HFResponseObject] | None,
    stats_result: RunStatistics | None,
    extension: str,
    destination: str,
    labels: dict[str, str] | None = None,
) -> bool:
    if not analysis_result and not stats_result:
        print("Nothing to write: no analysis results and no execution statistics.")
        return False
    try:
        dest_dir = resolve_destination(destination)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / f"{output_filename}"

        records = build_item_records(analysis_result, stats_result, labels)
        run_block = build_run_block(stats_result) if stats_result else {}

        if extension == "json":
            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump({"run": run_block, "result": records}, f, indent=2)

        elif extension in ("yaml", "yml"):
            with open(dest_path, "w", encoding="utf-8") as f:
                yaml.safe_dump({"run": run_block, "result": records}, f)

        elif extension == "csv":
            with open(dest_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=ITEM_CSV_FIELDS)
                writer.writeheader()
                for entry in records:
                    writer.writerow({field: _csv_value(entry.get(field)) for field in ITEM_CSV_FIELDS})
        else:
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write("\n".join(format_text_response(entry) for entry in records))

        print(f"Output has been written to {dest_path}")
        if stats_result:
            append_execution_stats(stats_result, destination)
        return True
    except OSError as e:
        print(f"An error occurred: {e}")
    return False


def format_text_response(response: dict) -> str:
    lines = [f"Name: {response['name']}", f"Classification: {response['classification']}"]
    if response.get("evidence"):
        lines.append(f"Evidence: {response['evidence']}")
    if response.get("confidence") is not None:
        lines.append(f"Confidence: {response['confidence']:.2%}")
    if response.get("fake_score") is not None:
        lines.append(f"P(DEEPFAKE): {response['fake_score']:.2%}")
    if response.get("raw_label"):
        lines.append(f"Raw label: {response['raw_label']}")
    if response.get("label") is not None:
        lines.append(f"Label: {response['label']}")
    if response.get("execution_time") is not None:
        lines.append(f"Execution time: {response['execution_time']:.3f}s")
    if response.get("success") is False:
        lines.append(f"Failed: {response.get('error') or 'unknown error'}")
    return "\n".join(lines) + "\n"


def write_output_to_stdout(
    analysis_result: list[ResponseObject] | list[HFResponseObject],
    stats_result: RunStatistics | None = None,
    destination: str | None = None,
    as_text: bool = True,
) -> bool:
    if not analysis_result:
        print("Analysis result was not provided, exiting...")
        return False

    records = build_item_records(analysis_result, stats_result)
    if as_text:
        for entry in records:
            print("\n" + format_text_response(entry))
    else:
        print(f"{records}")
    # Statistics were previously only logged on the file-output path, so stdout-only runs
    # left no trace in statistics.csv at all.
    if stats_result:
        append_execution_stats(stats_result, destination)
    return True


def append_execution_stats(stats: RunStatistics, destination: str | None = None) -> bool:
    """Appends a single row per run to statistics.csv."""
    try:
        log_path = resolve_statistics_path(destination)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        timings = [item.execution_time for item in stats.items]
        mean_time = sum(timings) / len(timings) if timings else None
        p95_time = None
        if timings:
            ordered = sorted(timings)
            index = min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))
            p95_time = ordered[index]
        throughput = (len(stats.items) / stats.total_execution_time) if stats.total_execution_time > 0 else None
        succeeded = sum(1 for item in stats.items if item.success)

        row = {field: getattr(stats, field, None) for field in STATISTIC_LOG_FIELDS}
        row.update(
            {
                "dataset": stats.dataset or "",
                "labels_file": stats.labels_file or "",
                "positive_label": stats.positive_label or "",
                "number_succeeded": succeeded,
                "number_failed": len(stats.items) - succeeded,
                "model_loading_time": stats.model_loading_time if stats.model_loading_time is not None else "",
                "mean_item_execution_time": mean_time if mean_time is not None else "",
                "p95_item_execution_time": p95_time if p95_time is not None else "",
                "throughput_items_per_sec": throughput if throughput is not None else "",
            }
        )

        write_header = not log_path.exists()
        if not write_header:
            # Appending rows whose field order differs from the existing header would silently
            # shift every column, so refuse instead of corrupting the file.
            with open(log_path, "r", encoding="utf-8", newline="") as f:
                existing = next(csv.reader(f), None)
            if existing != STATISTIC_LOG_FIELDS:
                print(
                    f"{log_path} has an incompatible header and was not appended to. "
                    f"Move it aside to start a new statistics log."
                )
                return False

        with open(log_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=STATISTIC_LOG_FIELDS)
            if write_header:
                writer.writeheader()
            writer.writerow({field: _csv_value(row.get(field)) for field in STATISTIC_LOG_FIELDS})
        return True
    except OSError as e:
        print(e)
        return False
