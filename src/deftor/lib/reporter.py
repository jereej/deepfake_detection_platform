# This file turns the analysis files into a dataset-wise model comparison report.
#
# Each analysis file written by the outputter is self-contained: a "run" block with the
# run-level metadata and a "result" list with one record per media file. Nothing is read
# from statistics.csv and nothing is parsed out of the filename, so models can be compared
# per dataset without any manual bookkeeping.
#
# DEEPFAKE is the positive class throughout.
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

# True positive rate is reported at these fixed false positive rates.
#
# Only targets the evaluation sets can actually express are listed. With n negatives the
# finest false positive rate a dataset can show is 1/n, and the thesis datasets have roughly
# 41-53 negatives each, i.e. a floor of about 0.02. Targets of 0.001 and 0.01 would therefore
# be unresolvable everywhere and always render as n/a. Raise these only if the evaluation
# sets grow; 0.05 and 0.10 are the low-FPR operating points these datasets can support.
FPR_TARGETS: tuple[float, ...] = (0.05, 0.10)

METRIC_COLUMNS = [
    "n",
    "tp",
    "tn",
    "fp",
    "fn",
    "accuracy",
    "precision",
    "recall",
    "f1",
    "auroc",
    "auprc",
    *[f"tpr@fpr{target:g}" for target in FPR_TARGETS],
]

# Only items with both a ground-truth label and a prediction can be scored at all.
SCORED_COLUMNS = ["y_true", "y_pred", "fake_score"]


def _safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator <= 0:
        return None
    return numerator / denominator


def load_analysis(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def iter_analyses(analyses_dir: str | Path) -> list[dict[str, Any]]:
    """Loads every analysis file, skipping (and reporting) unreadable ones."""
    analyses_dir = Path(analyses_dir)
    if not analyses_dir.exists():
        print(f"Error: analyses directory not found: {analyses_dir}")
        return []

    analyses: list[dict[str, Any]] = []
    legacy: list[str] = []
    for path in sorted(analyses_dir.glob("*.json")):
        try:
            analysis = load_analysis(path)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Warning: skipping {path.name}, could not be read ({e})")
            continue
        if not isinstance(analysis.get("run"), dict) or "result" not in analysis:
            # Written before the run block existed, so there is no dataset, model or score
            # to report on. Counting it as one anonymous row would hide that.
            legacy.append(path.name)
            continue
        analyses.append(analysis)

    if legacy:
        print(
            f"Warning: skipped {len(legacy)} analysis file(s) in the old format with no run "
            f"metadata, e.g. {', '.join(legacy[:3])}. Re-run those analyses to include them."
        )
    if not analyses:
        print(f"Warning: no analysis files found in {analyses_dir}")
    return analyses


def label_to_binary(raw_label: Any, positive_label: Any) -> int | None:
    """Maps a ground-truth label onto 1 (DEEPFAKE) / 0 (REAL).

    The positive label is whatever --positive-label said for that dataset, which may be a
    number ("1") or a word ("fake"). Exact match wins; anything unrecognised returns None so
    the item is excluded rather than silently counted as REAL.
    """
    if raw_label is None or positive_label is None:
        return None
    raw = str(raw_label).strip()
    positive = str(positive_label).strip()
    if not raw:
        return None
    if positive and raw.casefold() == positive.casefold():
        return 1
    if raw == "1":
        return 1
    if raw == "0":
        return 0
    return None


def classification_to_binary(classification: Any) -> int | None:
    if not isinstance(classification, str):
        return None
    text = classification.strip().upper()
    if "DEEPFAKE" in text:
        return 1
    if "REAL" in text:
        return 0
    return None


def _run_field(run: dict[str, Any], key: str, default: Any = "") -> Any:
    value = run.get(key, default)
    return default if value is None else value


def extract_rows(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    """Flattens one analysis file into per-item rows tagged with the run metadata."""
    run = analysis.get("run") if isinstance(analysis.get("run"), dict) else {}
    positive_label = run.get("positive_label")

    rows: list[dict[str, Any]] = []
    for entry in analysis.get("result") or []:
        if not isinstance(entry, dict):
            continue
        score = entry.get("fake_score")
        if score is not None:
            try:
                score = float(score)
            except TypeError, ValueError:
                score = None
        rows.append(
            {
                "model": _run_field(run, "model", "unknown"),
                "backend": _run_field(run, "backend", "unknown"),
                "media_type": _run_field(run, "media_type", "unknown"),
                "dataset": _run_field(run, "dataset") or "unlabelled",
                "file_name": entry.get("name") or "unknown",
                "y_true": label_to_binary(entry.get("label"), positive_label),
                "y_pred": classification_to_binary(entry.get("classification")),
                "fake_score": score,
                "execution_time": entry.get("execution_time"),
                "success": entry.get("success"),
            }
        )
    return rows


def build_item_frame(analyses: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for analysis in analyses:
        rows.extend(extract_rows(analysis))
    return pd.DataFrame(rows)


def compute_hard_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, Any]:
    """Accuracy/precision/recall/F1 plus the confusion matrix. Works for every backend."""
    metrics: dict[str, Any] = dict.fromkeys(METRIC_COLUMNS)
    metrics.update({"n": 0, "tp": 0, "tn": 0, "fp": 0, "fn": 0})
    if y_true.size == 0:
        return metrics

    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))

    precision = _safe_divide(tp, tp + fp)
    recall = _safe_divide(tp, tp + fn)
    metrics.update(
        {
            "n": int(y_true.size),
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "accuracy": _safe_divide(tp + tn, y_true.size),
            "precision": precision,
            "recall": recall,
            "f1": _safe_divide(2 * precision * recall, precision + recall)
            if precision is not None and recall is not None
            else None,
        }
    )
    return metrics


def compute_threshold_metrics(y_true: np.ndarray, y_score: np.ndarray) -> dict[str, Any]:
    """AUROC/AUPRC/TPR@FPR. Needs a per-item score, so it is only available for backends
    that report one (Hugging Face). Returns None everywhere when scores are missing."""
    metrics: dict[str, Any] = dict.fromkeys(METRIC_COLUMNS)
    metrics.update({"n": 0, "tp": 0, "tn": 0, "fp": 0, "fn": 0})

    usable = np.isfinite(y_score)
    y_true = y_true[usable]
    y_score = y_score[usable]
    if y_score.size == 0:
        return metrics
    # A single-class ground truth leaves AUROC/AUPRC undefined.
    if np.unique(y_true).size < 2:
        return metrics

    metrics["auroc"] = float(roc_auc_score(y_true, y_score))
    metrics["auprc"] = float(average_precision_score(y_true, y_score))

    # Sweep every distinct score as a threshold and keep the best true positive rate that
    # stays within the false positive budget.
    #
    # This is done by hand rather than by reading points off roc_curve because roc_curve
    # collapses tied scores into a single jump. When a model emits few distinct scores the
    # curve can skip over the whole region of interest, which made a genuinely bad model
    # report as n/a instead of 0. Every candidate threshold is a real operating point, so
    # 0.0 here is a true measurement and not missing data.
    negatives = float(np.sum(y_true == 0))
    order = np.argsort(-y_score, kind="stable")
    sorted_scores = y_score[order]
    sorted_true = y_true[order]
    # Cumulative counts as the threshold moves down through the ranked scores.
    positives_so_far = np.cumsum(sorted_true == 1)
    negatives_so_far = np.cumsum(sorted_true == 0)
    # Only the end of each run of equal scores is a realisable threshold.
    last_of_run = np.r_[sorted_scores[1:] != sorted_scores[:-1], True]

    total_positives = int(positives_so_far.max())
    for target in FPR_TARGETS:
        key = f"tpr@fpr{target:g}"
        if negatives == 0:
            metrics[key] = None
            continue
        # With n negatives the finest expressible false positive rate is 1/n. A budget
        # below that floor cannot be measured, so report n/a rather than a number that
        # would only be measuring the trivial "flag nothing" threshold.
        if target < 1.0 / negatives:
            metrics[key] = None
            continue
        false_positive_rate = negatives_so_far[last_of_run] / negatives
        within = false_positive_rate <= target
        best = float(positives_so_far[last_of_run][within].max() / total_positives) if within.any() else 0.0
        metrics[key] = best
    return metrics


def summarize_group(group: pd.DataFrame, n_runs: int, n_datasets: int | None = None) -> dict[str, Any]:
    """Scores one (model, backend, dataset, media_type) group, pooling every repeat run."""
    row: dict[str, Any] = {
        "model": group["model"].iloc[0],
        "backend": group["backend"].iloc[0],
        "media_type": group["media_type"].iloc[0],
        "n_runs": n_runs,
    }
    if n_datasets is not None:
        row["dataset"] = f"all ({n_datasets})"
        row["n_datasets"] = n_datasets
    else:
        row["dataset"] = group["dataset"].iloc[0]

    labelled = group[group["y_true"].notna() & group["y_pred"].notna()]
    y_true = labelled["y_true"].to_numpy(dtype=int)
    y_pred = labelled["y_pred"].to_numpy(dtype=int)
    row.update(compute_hard_metrics(y_true, y_pred))

    scored = group[group["y_true"].notna() & group["fake_score"].notna()]
    if len(scored):
        threshold = compute_threshold_metrics(
            scored["y_true"].to_numpy(dtype=int),
            scored["fake_score"].to_numpy(dtype=float),
        )
        for key in ("auroc", "auprc", *(f"tpr@fpr{target:g}" for target in FPR_TARGETS)):
            row[key] = threshold[key]
    return row


def summarize_by_dataset(items: pd.DataFrame, run_counts: dict[tuple[str, ...], int]) -> pd.DataFrame:
    """The primary comparison: one row per model per dataset, repeats pooled."""
    columns = ["model", "backend", "dataset", "media_type", "n_runs", *METRIC_COLUMNS]
    if items.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    keys = ["model", "backend", "dataset", "media_type"]
    for key, group in items.groupby(keys, sort=False):
        rows.append(summarize_group(group, n_runs=run_counts.get(key, 1)))
    summary = pd.DataFrame(rows)
    return summary.sort_values(["dataset", "model", "backend"]).reset_index(drop=True)[columns]


def summarize_by_model(items: pd.DataFrame, run_counts: dict[tuple[str, ...], int]) -> pd.DataFrame:
    """Rolls the per-dataset rows up to one row per model and media type."""
    columns = ["model", "backend", "dataset", "media_type", "n_datasets", "n_runs", *METRIC_COLUMNS]
    if items.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    keys = ["model", "backend", "media_type"]
    for key, group in items.groupby(keys, sort=False):
        # A model can have several runs per dataset; sum them for the pooled row.
        n_runs = sum(count for k, count in run_counts.items() if k[0] == key[0] and k[1] == key[1] and k[3] == key[2])
        rows.append(summarize_group(group, n_runs=n_runs, n_datasets=group["dataset"].nunique()))
    summary = pd.DataFrame(rows)
    return summary.sort_values(["media_type", "model", "backend"]).reset_index(drop=True)[columns]


def format_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    display = frame.copy()
    for column in ("accuracy", "precision", "recall", "f1", "auroc", "auprc"):
        if column in display.columns:
            display[column] = display[column].map(lambda v: "n/a" if pd.isna(v) else f"{v:.1%}")
    for target in FPR_TARGETS:
        column = f"tpr@fpr{target:g}"
        if column in display.columns:
            display[column] = display[column].map(lambda v: "n/a" if pd.isna(v) else f"{v:.1%}")
    return display


def _table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No scored data._"
    return format_metrics(frame).to_markdown(index=False)


def _coverage_note(items: pd.DataFrame) -> list[str]:
    if items.empty:
        return []
    total = len(items)
    unlabelled = int(items["y_true"].isna().sum())
    unscored = int(items["fake_score"].isna().sum())
    notes = [f"Scored {total - unlabelled}/{total} items that carried both a label and a prediction."]
    if unlabelled:
        notes.append(f"{unlabelled} item(s) had no usable label and were left out of the metrics.")
    if unscored:
        notes.append(
            f"{unscored} item(s) had no fake_score, so AUROC/AUPRC/TPR@FPR are n/a for them. "
            "Ollama models do not report a score, so they only get the hard metrics."
        )
    if not items.empty and items["fake_score"].notna().any():
        notes.append(
            "TPR@FPR is the highest true positive rate reachable at any threshold that stays "
            "within the given false positive budget, so 0% is a real measurement of a model that "
            "catches nothing without false alarms. It is n/a only when the budget is finer than "
            f"the dataset can express (1/n with n negatives, here about {1 / _min_negatives(items):.2f})."
        )
    return notes


def _min_negatives(items: pd.DataFrame) -> float:
    negatives = float(items["y_true"].eq(0).sum())
    return max(negatives, 1.0)


def dataset_sections(by_dataset: pd.DataFrame, items: pd.DataFrame) -> list[str]:
    """One table per dataset, so models can only be compared within a dataset.

    Each dataset gets its own section rather than a single wide table because pooling
    datasets into one row makes a model evaluated on an easy set look better than one
    evaluated on every set. Per-dataset tables are also the only place the numbers are
    directly comparable.
    """
    if by_dataset.empty:
        return []

    lines: list[str] = ["## Per dataset", ""]
    for dataset, group in by_dataset.groupby("dataset", sort=True):
        media_types = sorted(set(group["media_type"]))
        described = "/".join(media_types) if media_types else "unknown"

        # Every model was run over the same items, so counting rows would multiply the
        # dataset size by the number of models. Deduplicate on the media file name.
        rows = items[items["dataset"] == dataset]
        unique = rows.drop_duplicates(subset=["file_name"])
        negatives = int(unique["y_true"].eq(0).sum())
        positives = int(unique["y_true"].eq(1).sum())

        detail = f"{described}, {len(unique)} item(s)"
        if negatives or positives:
            detail += f" ({positives} DEEPFAKE / {negatives} REAL)"
        if len(group) > 1:
            detail += f", {len(group)} model(s)"
        lines += [
            f"### {dataset}",
            "",
            f"_{detail}. Repeat runs of a model are pooled into one row._",
            "",
            # dataset, media_type and backend are constant or near-constant within a
            # section, so drop the two that no longer distinguish the rows.
            _table(group.drop(columns=["dataset", "media_type", "backend"])),
            "",
        ]
    return lines


def build_markdown_report(
    by_dataset: pd.DataFrame,
    by_model: pd.DataFrame,
    items: pd.DataFrame,
    title: str,
) -> str:
    lines = [
        f"# {title}",
        "",
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
        "DEEPFAKE is the positive class. One table per dataset follows; use those to compare",
        "models. Repeat runs of the same model on the same dataset are pooled into one row, so",
        "`n` is the number of scored items across all of them.",
        "",
        *dataset_sections(by_dataset, items),
        "## Models per media type",
        "",
        "Datasets are pooled here, so a model that was only ever run on one dataset can look",
        "better than one evaluated everywhere. Use the per-dataset tables above for comparisons.",
        "",
        _table(by_model),
        "",
    ]
    notes = _coverage_note(items)
    if notes:
        lines += ["## Coverage", "", *[f"- {note}" for note in notes], ""]
    return "\n".join(lines)


def count_runs(analyses: list[dict[str, Any]]) -> dict[tuple[str, ...], int]:
    """Counts how many analysis files contributed to each group, so `n_runs` is real."""
    counts: dict[tuple[str, ...], int] = {}
    for analysis in analyses:
        run = analysis.get("run") if isinstance(analysis.get("run"), dict) else {}
        key = (
            _run_field(run, "model", "unknown"),
            _run_field(run, "backend", "unknown"),
            _run_field(run, "dataset") or "unlabelled",
            _run_field(run, "media_type", "unknown"),
        )
        if not analysis.get("result"):
            continue
        counts[key] = counts.get(key, 0) + 1
    return counts


def write_report(
    analyses_dir: str | Path | None = None,
    output_path: str | Path | None = None,
    title: str = "Deftor Model Performance Report",
) -> Path:
    """Reads every analysis file and writes the dataset-wise comparison report."""
    analyses_path = Path(analyses_dir) if analyses_dir else Path.cwd() / "analyses"
    output = Path(output_path) if output_path else Path.cwd() / "report.md"

    analyses = iter_analyses(analyses_path)
    items = build_item_frame(analyses)
    run_counts = count_runs(analyses)

    by_dataset = summarize_by_dataset(items, run_counts)
    by_model = summarize_by_model(items, run_counts)

    output.write_text(build_markdown_report(by_dataset, by_model, items, title), encoding="utf-8")
    print(f"Report written to {output.resolve()}")
    if by_dataset.empty:
        print("No labelled results found. Re-run the analyses with --labels to get metrics.")
    return output
