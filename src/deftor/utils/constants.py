# Constants that are used in various parts of DEFTOR
from typing import Literal

# Media type extensions map
MEDIA_EXTENSIONS: dict[Literal["image", "audio", "video"], set[str]] = {
    "image": {".jpg", ".jpeg", ".png", ".webp", ".bmp"},
    "audio": {".wav", ".mp3"},
    "video": {".mp4", ".mov", ".avi"}
}

# Task type map for Hugging Face pipeline
TASK_TYPE: dict[Literal["image", "audio", "video"], str] = {
    "image": "image-classification",
    "audio": "audio-classification",
    "video": "video-classification"
}

# Default prompt for Ollama models
DEFAULT_PROMPT = """DEEPFAKE / AI-GENERATED IMAGE DETECTION

Analyze the given image for evidence of AI generation.

Provide:
- classification
- evidence: 2-4 concise, specific, observable details

Do not explain your reasoning outside these fields."""

# Default options for Ollama models
DEFAULT_OPTIONS = {"num_predict": 2048}

FAKE_KEYWORDS: tuple[str, ...] = ("fake", "deepfake", "synthetic", "generated", "spoof", "ai")

LABEL_OVERRIDES: dict[str, dict[str, str]] = {
    # "org/model-name": {"spoof": "DEEPFAKE", "bonafide": "REAL"},
}