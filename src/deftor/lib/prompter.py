# This file contains the main logic for dealing with LLMs/AI Models
# As DEFTOR supports both ollama and huggingface models, both cases
# are handled in this file.

import time
from ollama import chat, ResponseError
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from pathlib import Path
from ..utils import constants


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


def prompt_model(
    backend: str,
    model: str,
    options: dict | None = None,
    image_paths: list[str] | None = None
) -> list[ResponseObject] | list[HFResponseObject] | None: # tähän se hf responseobject
    print(f"DEBUG: Backend is: {backend}")
    if backend == "ollama":
        return image_prompt_ollama(model=model, image_paths=image_paths, options=options)
    elif backend == "huggingface":
        if not image_paths:
            return []
        ext = Path(image_paths[0]).suffix.lower()
        media_type = next(
            (mt for mt, exts in constants.MEDIA_EXTENSIONS.items() if ext in exts),
            None,
        )
        if media_type is None:
            print(f"Unsupported file extension: {ext}")
            return []
        return huggingface_prompt(media_type=media_type, model=model, media_paths=image_paths)

def normalize_label(label: str, model:str) -> Literal["DEEPFAKE", "REAL"]:
    overrides = constants.LABEL_OVERRIDES.get(model)
    if overrides and label in overrides:
        return overrides[label]
    return "DEEPFAKE" if any(k in label.lower() for k in constants.FAKE_KEYWORDS) else "REAL"

def image_prompt_ollama(
    model: str,
    options: dict | None = None,
    image_paths: list[str] | None = None,
) -> list[ResponseObject]:
    options = options or constants.DEFAULT_OPTIONS
    results: list[ResponseObject] = []
    print(f"DEBUG: Given options: {options}")
    try:
        start = time.perf_counter()
        if image_paths:
            for image in image_paths:
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
                        options=options
                    )
                    # DEBUG PRINT
                    # print(f"--- RAW RESPONSE: ---\n\n{response.message.content}")
                    res_obj = ResponseObject.model_validate_json(str(response.message.content))
                    res_obj.image_name = Path(image).name
                    results.append(res_obj)
                except ValidationError:
                    print(f"Image {Path(image).name} failed, skipping")
                    continue
        end = time.perf_counter()
        exec_time = end - start
        print(f"Execution time: {exec_time}")
        return results
    except ResponseError as e:
        if e.status_code == 400:
            print(f"Some of the given images were broken {', '.join(image_paths or [])}. Please check the files.")
    return results


def huggingface_prompt(
    media_type: Literal["image", "audio", "video"],
    model: str,
    media_paths: list[str]
) -> list[HFResponseObject]:
    from transformers import pipeline
    # transformer import is kept here due to it making deftor laggy
    task = constants.TASK_TYPE.get(media_type)
    if task is None:
        raise ValueError(f"Unsupported media type: {media_type!r}")
    pipe = pipeline(task, model=model)
    results: list[HFResponseObject] = []
    
    start = time.perf_counter()
    for media in media_paths:
        try:
            output = pipe(media)
            # Filters out the "losing" result
            # e.g. {"fake": 0.8, "real": 0.2} => {"fake": 0.8}
            top = max(output, key=lambda x: x["score"])
            results.append(
                HFResponseObject(
                    media_name=Path(media).name,
                    media_type=media_type,
                    classification=normalize_label(top["label"], model),
                    confidence=top["score"],
                    raw_label=top["label"]
                )
            )
        except Exception as e:
            print(f"Media {Path(media).name} failed: {e}")
            continue
    print(f"results are: {chr(10).join(r.model_dump_json() for r in results)}")
    print(f"Exec time: {time.perf_counter() - start}")
    return results
    