import time
from ollama import chat, ResponseError
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from pathlib import Path


class ResponseObject(BaseModel):
    image_name: str = Field(description="Filename of the image, example: image.png")
    classification: Literal["DEEPFAKE", "REAL IMAGE"] = Field(
        description="Result of the analysis, DEEPFAKE or REAL IMAGE"
    )
    evidence: list[str] = Field(description="Found evidence supporting the result of the analysis")


DEFAULT_PROMPT = """DEEPFAKE / AI-GENERATED IMAGE DETECTION

Analyze the given image for evidence of AI generation.

Provide:
- classification
- evidence: 2-4 concise, specific, observable details

Do not explain your reasoning outside these fields."""
DEFAULT_OPTIONS = {"num_predict": 2048}


def image_prompt_ollama(
    model: str,
    # options: dict | None = None,
    image_paths: list[str] | None = None,
) -> list[ResponseObject]:
    # options = options or DEFAULT_OPTIONS
    results: list[ResponseObject] = []
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
                                "content": DEFAULT_PROMPT,
                                "images": [image],
                            }
                        ],
                        format=ResponseObject.model_json_schema(),
                        # options=options
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
