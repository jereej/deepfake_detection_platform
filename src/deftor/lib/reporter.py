# The file with all the statistical analysis stuff
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
from ..utils import constants
from ..lib.prompter import RunStatistics, ItemStatistics
from datetime import datetime, timezone


def _format_timestamp(ts: str) -> str:
    dt = datetime.fromisoformat(ts).astimezone()  # converts to local system timezone
    return dt.strftime("%B %d, %Y at %H:%M:%S %Z")


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


def load_dataframe(filepath: str | Path | None = None) -> pd.DataFrame:
    if not filepath:
        filepath = constants.STATISTIC_LOG_PATH
    df = pd.read_csv(filepath)

    # Only the `error` column needs NaN -> None (for pydantic's str | None).
    # Leave numeric columns as proper numeric dtypes (float64/int64/bool)
    # so pandas/numpy/scipy operations downstream work correctly.
    if "error" in df.columns:
        df["error"] = df["error"].astype(object).where(pd.notnull(df["error"]), None)

    return df


# --------------------------------------------------------------------------
# Run-wise grouping (mirrors RunStatistics exactly, like before)
# --------------------------------------------------------------------------


def list_runs(df: pd.DataFrame) -> list[RunStatistics]:
    runs: list[RunStatistics] = []
    for ts, run_df in df.groupby("timestamp", sort=False):
        items = [
            ItemStatistics(**item)  # type: ignore[arg-type]
            for item in run_df[["file_name", "file_size_in_bytes", "execution_time", "success", "error"]].to_dict(
                "records"
            )
        ]
        first = run_df.iloc[0]
        runs.append(
            RunStatistics(
                timestamp=str(ts),
                backend=first["backend"],
                model=first["model"],
                media_type=first["media_type"],
                number_of_items=int(first["number_of_items"]),
                total_execution_time=first["total_execution_time"],
                model_loading_time=first["model_loading_time"],
                items=items,
            )
        )
    return runs


# --------------------------------------------------------------------------
# Image-wise and model-wise groupings (aggregated views, not RunStatistics)
# --------------------------------------------------------------------------


def image_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("file_name", sort=False)
        .agg(
            file_size_in_bytes=("file_size_in_bytes", "first"),
            n_runs=("timestamp", "nunique"),
            avg_execution_time=("execution_time", "mean"),
            min_execution_time=("execution_time", "min"),
            max_execution_time=("execution_time", "max"),
            success_rate=("success", "mean"),
        )
        .reset_index()
        .sort_values("file_name")
    )


def model_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("model", sort=False)
        .agg(
            backend=("backend", "first"),
            n_runs=("timestamp", "nunique"),
            n_items=("file_name", "count"),
            avg_execution_time=("execution_time", "mean"),
            avg_model_loading_time=("model_loading_time", "mean"),
            success_rate=("success", "mean"),
        )
        .reset_index()
    )


def image_model_pivot(df: pd.DataFrame, value: str = "execution_time", aggfunc="mean") -> pd.DataFrame:
    return df.pivot_table(index="file_name", columns="model", values=value, aggfunc=aggfunc)


# --------------------------------------------------------------------------
# Model speed statistics
# --------------------------------------------------------------------------


def model_speed_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Descriptive statistics of execution_time per model."""
    return (
        df.groupby("model", sort=False)["execution_time"]
        .agg(
            n="count",
            mean="mean",
            median="median",
            std="std",
            min="min",
            max="max",
            q25=lambda s: s.quantile(0.25),
            q75=lambda s: s.quantile(0.75),
        )
        .assign(cv=lambda d: d["std"] / d["mean"])  # coefficient of variation: consistency, not just speed
        .reset_index()
    )


# --------------------------------------------------------------------------
# Pairwise model comparison (paired, since same images are reused)
# --------------------------------------------------------------------------


def _image_level_means(df: pd.DataFrame) -> pd.DataFrame:
    """Average execution_time per (model, file_name) — collapses repeated runs first."""
    return (
        df.groupby(["model", "file_name"], sort=False)["execution_time"]
        .mean()
        .reset_index()
        .pivot(index="file_name", columns="model", values="execution_time")
    )


def pairwise_model_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """
    For every pair of models, run a paired comparison on execution_time
    across the images both models processed in common.

    Uses Wilcoxon signed-rank test (paired, non-parametric) rather than a
    paired t-test, since execution times are typically right-skewed
    (occasional slow outliers, e.g. cold model loads) and small sample
    sizes make normality assumptions shaky.
    """
    wide = _image_level_means(df)
    models = list(wide.columns)
    rows = []

    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            m1, m2 = models[i], models[j]
            paired = wide[[m1, m2]].dropna()
            if len(paired) < 2:
                continue

            diffs = paired[m1] - paired[m2]
            try:
                _, p_value = stats.wilcoxon(paired[m1], paired[m2])
            except ValueError:
                # all differences are zero, or too few samples
                _, p_value = np.nan, np.nan

            # rank-biserial correlation as effect size (paired, non-parametric)
            n = len(diffs)
            effect_size = (diffs > 0).sum() / n - (diffs < 0).sum() / n if n else np.nan

            rows.append(
                {
                    "model_a": m1,
                    "model_b": m2,
                    "n_shared_images": n,
                    "mean_diff_seconds": diffs.mean(),
                    "faster_model": m1 if diffs.mean() < 0 else m2,
                    "p_value": p_value,
                    "significant_at_0.05": p_value < 0.05 if pd.notnull(p_value) else None,
                    "effect_size": effect_size,
                }
            )

    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Execution time vs file size correlation, per model
# --------------------------------------------------------------------------


def size_vs_time_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Pearson and Spearman correlation between file size and execution time, per model."""
    rows = []
    for model, group in df.groupby("model", sort=False):
        if len(group) < 3:
            continue
        pearson_r, pearson_p = stats.pearsonr(group["file_size_in_bytes"], group["execution_time"])
        spearman_r, spearman_p = stats.spearmanr(group["file_size_in_bytes"], group["execution_time"])
        rows.append(
            {
                "model": model,
                "n": len(group),
                "pearson_r": pearson_r,
                "pearson_p": pearson_p,
                "spearman_r": spearman_r,
                "spearman_p": spearman_p,
            }
        )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Markdown report
# --------------------------------------------------------------------------


def _run_to_markdown(run: RunStatistics) -> str:
    lines = [
        f"### Run: {_format_timestamp(run.timestamp)}",
        "",
        f"- **Backend:** {run.backend}",
        f"- **Model:** {run.model}",
        f"- **Media type:** {run.media_type}",
        f"- **Items:** {run.number_of_items}",
        f"- **Total execution time:** {run.total_execution_time:.3f}s",
        f"- **Model loading time:** {run.model_loading_time if run.model_loading_time is not None else 'n/a'}",
        "",
        "| File | Size (bytes) | Execution time (s) | Success | Error |",
        "|---|---|---|---|---|",
    ]
    for item in run.items:
        lines.append(
            f"| {item.file_name} | {item.file_size_in_bytes} | {item.execution_time:.3f} "
            f"| {'✅' if item.success else '❌'} | {item.error or ''} |"
        )
    lines.append("")
    return "\n".join(lines)


def _df_to_markdown(df: pd.DataFrame) -> str:
    df = df.copy()
    float_cols = df.select_dtypes(include="float").columns
    df[float_cols] = df[float_cols].round(3)
    if "success_rate" in df.columns:
        df["success_rate"] = df["success_rate"].map(lambda x: f"{x:.0%}" if pd.notnull(x) else "")
    return df.to_markdown(index=False)


def build_markdown_report(
    runs: list[RunStatistics],
    images_df: pd.DataFrame,
    models_df: pd.DataFrame,
    pivot_df: pd.DataFrame,
    speed_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    correlation_df: pd.DataFrame,
    title: str = "Deftor Analysis Report",
) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_items = sum(r.number_of_items for r in runs)

    parts = [
        f"# {title}",
        "",
        f"_Generated {generated_at} · {total_items} items across {len(runs)} runs_",
        "",
        "## Runs",
        "",
    ]
    parts.extend(_run_to_markdown(run) for run in runs)

    parts += [
        "## Images",
        "",
        "One row per image, aggregated across every run/model that processed it.",
        "",
        _df_to_markdown(images_df),
        "",
        "## Model Comparison per Image",
        "",
        "Execution time (seconds) per image, broken down by model.",
        "",
        pivot_df.round(3).to_markdown(),
        "",
        "## Models",
        "",
        "One row per model, aggregated across all runs.",
        "",
        _df_to_markdown(models_df),
        "",
    ]

    parts += [
        "## Model Speed Statistics",
        "",
        _df_to_markdown(speed_df),
        "",
        "## Pairwise Model Comparison",
        "",
        "Paired Wilcoxon signed-rank test on execution time, matched by image. "
        "`effect_size` ranges from -1 to 1: values near ±1 mean one model is "
        "almost always faster on shared images; values near 0 mean it's a toss-up.",
        "",
        _df_to_markdown(comparison_df)
        if not comparison_df.empty
        else "_Not enough shared images between any pair of models yet._",
        "",
        "## Execution Time vs File Size",
        "",
        "Correlation between image file size and execution time, per model.",
        "",
        _df_to_markdown(correlation_df) if not correlation_df.empty else "_Not enough data points per model yet._",
        "",
    ]
    return "\n".join(parts)


def write_markdown_report(
    filepath: str | Path | None = None,
    output_path: str | Path | None = None,
    title: str = "Deftor Analysis Report",
) -> Path:
    if output_path is None:
        output_path = Path.cwd() / "report.md"
    output_path = Path(output_path)

    df = load_dataframe(filepath)
    runs = list_runs(df)
    images_df = image_summary(df)
    models_df = model_summary(df)
    pivot_df = image_model_pivot(df)
    speed_df = model_speed_stats(df)
    comparison_df = pairwise_model_comparison(df)
    correlation_df = size_vs_time_correlation(df)

    md = build_markdown_report(
        runs, images_df, models_df, pivot_df, speed_df, comparison_df, correlation_df, title=title
    )
    output_path.write_text(md, encoding="utf-8")
    return output_path


# --------------------------------------------------------------------------
# CLI entry point
# --------------------------------------------------------------------------


def create_report(filepath: str | Path | None = None):
    out = write_markdown_report(filepath)
    print(f"Report written to {out.resolve()}")
