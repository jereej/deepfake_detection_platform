# This file contains the main logic for dealing with LLMs/AI Models
# As DEFTOR supports both ollama and huggingface models, both cases
# are handled in this file.

import time
from datetime import datetime, timezone
from ollama import chat, ResponseError
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from pathlib import Path
from ..utils import constants
from beaupy.spinners import Spinner


class ResponseObject(BaseModel):
    image_name: str = Field(description="Filename of the image, example: image.png")
    classification: Literal["DEEPFAKE", "REAL IMAGE"] = Field(
        description="Result of the analysis, DEEPFAKE or REAL IMAGE"
    )
    evidence: list[str] = Field(description="Found evidence supporting the result of the analysis")


class HFResponseObject(BaseModel):
    media_name: str = Field(description="Filename of the media, e.g. video.mp4 or sound.mp3")
    media_type: Literal["image", "audio", "video"]
    classification: Literal["DEEPFAKE", "REAL"]
    confidence: float = Field(description="Model's confidence score")
    raw_label: str = Field(description="Unmodified label returned by the model")


class ItemStatistics(BaseModel):
    file_name: str
    file_size_in_bytes: int
    execution_time: float
    success: bool
    error: str | None = None


class RunStatistics(BaseModel):
    timestamp: str
    backend: Literal["ollama", "huggingface"]
    model: str
    media_type: str | None = None
    number_of_items: int
    total_execution_time: float
    model_loading_time: float | None = None
    items: list[ItemStatistics]


def prompt_model(
    backend: str, model: str, options: dict | None = None, image_paths: list[str] | None = None
) -> tuple[list[ResponseObject], RunStatistics] | tuple[list[HFResponseObject], RunStatistics] | None:
    spinner = Spinner(constants.ANALYSIS_SPINNER_ANIMATION, "Analyzing...")
    if backend == "ollama":
        spinner.start()
        ollama_results, ollama_stats = image_prompt_ollama(model=model, image_paths=image_paths, options=options)
        spinner.stop()
        return ollama_results, ollama_stats
    elif backend == "huggingface":
        if not image_paths:
            return None
        ext = Path(image_paths[0]).suffix.lower()
        media_type = next(
            (mt for mt, exts in constants.MEDIA_EXTENSIONS.items() if ext in exts),
            None,
        )
        if media_type is None:
            print(f"Unsupported file extension: {ext}")
            return None
        spinner.start()
        hf_results, hf_stats = huggingface_prompt(media_type=media_type, model=model, media_paths=image_paths)
        spinner.stop()
        return hf_results, hf_stats


def normalize_label(label: str, model: str) -> Literal["DEEPFAKE", "REAL"]:
    return "DEEPFAKE" if any(k in label.lower() for k in constants.FAKE_KEYWORDS) else "REAL"


def image_prompt_ollama(
    model: str,
    options: dict | None = None,
    image_paths: list[str] | None = None,
) -> tuple[list[ResponseObject], RunStatistics]:

    options = options or constants.DEFAULT_OPTIONS
    results: list[ResponseObject] = []
    item_statistics: list[ItemStatistics] = []
    start = time.perf_counter()
    try:
        if image_paths:
            for image in image_paths:
                file_size = Path(image).stat().st_size if Path(image).exists() else 0
                item_start = time.perf_counter()
                try:
                    response = chat(
                        model=model,
                        messages=[
                            {
                                "role": "user",
                                "content": constants.DEFAULT_PROMPT,
                                "images": [image],
                            }
                        ],
                        format=ResponseObject.model_json_schema(),
                        options=options,
                    )
                    item_time = time.perf_counter() - item_start
                    res_obj = ResponseObject.model_validate_json(str(response.message.content))
                    res_obj.image_name = Path(image).name
                    results.append(res_obj)
                    item_statistics.append(
                        ItemStatistics(
                            file_name=Path(image).name,
                            file_size_in_bytes=file_size,
                            execution_time=item_time,
                            success=True,
                        )
                    )
                except ValidationError as e:
                    item_statistics.append(
                        ItemStatistics(
                            file_name=Path(image).name,
                            file_size_in_bytes=file_size,
                            execution_time=time.perf_counter() - item_start,
                            success=False,
                            error=str(e),
                        )
                    )
                    print(f"Image {Path(image).name} failed, skipping")
                    continue
    except ResponseError as e:
        if e.status_code == 400:
            print(f"Some of the given images were broken {', '.join(image_paths or [])}. Please check the files.")
    exec_time = time.perf_counter() - start
    stats = RunStatistics(
        timestamp=datetime.now(timezone.utc).isoformat(),
        backend="ollama",
        model=model,
        media_type="image",
        number_of_items=len(image_paths or []),
        total_execution_time=exec_time,
        model_loading_time=None,
        items=item_statistics,
    )
    return results, stats


def huggingface_prompt(
    media_type: Literal["image", "audio", "video"], model: str, media_paths: list[str]
) -> tuple[list[HFResponseObject], RunStatistics]:
    from transformers import pipeline

    # transformer import is kept here due to it making deftor laggy
    task = constants.TASK_TYPE.get(media_type)
    if task is None:
        raise ValueError(f"Unsupported media type: {media_type!r}")

    loading_start = time.perf_counter()
    pipe = pipeline(task, model=model)
    loading_time = time.perf_counter() - loading_start

    results: list[HFResponseObject] = []
    item_statistics: list[ItemStatistics] = []

    start = time.perf_counter()
    for media in media_paths:
        file_size = Path(media).stat().st_size if Path(media).exists() else 0
        item_start = time.perf_counter()
        try:
            output = pipe(media)
            item_time = time.perf_counter() - item_start
            # Capturing only the meaningful output
            # e.g. {"fake": 0.8, "real": 0.2} => {"fake": 0.8}
            top = max(output, key=lambda x: x["score"])
            print(f"output is: {output}")
            results.append(
                HFResponseObject(
                    media_name=Path(media).name,
                    media_type=media_type,
                    classification=normalize_label(top["label"], model),
                    confidence=top["score"],
                    raw_label=top["label"],
                )
            )
            item_statistics.append(
                ItemStatistics(
                    file_name=Path(media).name, file_size_in_bytes=file_size, execution_time=item_time, success=True
                )
            )
        except Exception as e:
            item_statistics.append(
                ItemStatistics(
                    file_name=Path(media).name,
                    file_size_in_bytes=file_size,
                    execution_time=time.perf_counter() - item_start,
                    success=False,
                    error=str(e),
                )
            )
            print(f"Media {Path(media).name} failed: {e}")
            continue
    total_execution_time = time.perf_counter() - start
    stats = RunStatistics(
        timestamp=datetime.now(timezone.utc).isoformat(),
        backend="huggingface",
        model=model,
        media_type=media_type,
        number_of_items=len(media_paths),
        total_execution_time=total_execution_time,
        model_loading_time=loading_time,
        items=item_statistics,
    )
    return results, stats
