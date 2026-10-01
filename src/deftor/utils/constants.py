# Constants that are used in various parts of DEFTOR
from typing import Literal
from pathlib import Path

# Media type extensions map
# NOTE: Some models might not be able to support specified types of media.
# For example Ollama models do not support .mp4 video files and are only able to
# sample videos frame-by-frame (i.e. image analysis)
MEDIA_EXTENSIONS: dict[Literal["image", "audio", "video", "text"], set[str]] = {
    "image": {".jpg", ".jpeg", ".png", ".webp", ".bmp"},
    "audio": {".wav", ".mp3"},
    "video": {".mp4", ".mov", ".avi"},
    "text": {".txt"},
}

# Task type map for Hugging Face pipeline
TASK_TYPE: dict[Literal["image", "audio", "video"], str] = {
    "image": "image-classification",
    "audio": "audio-classification",
    "video": "video-classification",
}

# Default prompt for Ollama models
DEFAULT_PROMPT = """DEEPFAKE / AI-GENERATED MEDIA DETECTION

Analyze the given media for evidence of AI generation.

Provide:
- classification
- evidence: 2-4 concise, specific, observable details

Do not explain your reasoning outside these fields."""

# Default options for Ollama models
DEFAULT_OPTIONS = {"num_predict": 8192}

# ... syntax allows >=1 items in a tuple
FAKE_KEYWORDS: tuple[str, ...] = ("fake", "deepfake", "synthetic", "generated", "spoof", "ai")

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

# Spinner animation sequence
ANALYSIS_SPINNER_ANIMATION: list[str] = [
    "🐶🔎      🖼️🎵📹📃",
    " 🐶🔎     🖼️🎵📹📃",
    "  🐶🔎    🖼️🎵📹📃",
    "   🐶🔎   🖼️🎵📹📃",
    "    🐶🔎  🖼️🎵📹📃",
    "     🐶🔎 🖼️🎵📹📃",
    "      🐶🔎🖼️🎵📹📃",
    "     🐶🔎 🖼️🎵📹📃",
    "    🐶🔎  🖼️🎵📹📃",
    "   🐶🔎   🖼️🎵📹📃",
    "  🐶🔎    🖼️🎵📹📃",
    " 🐶🔎     🖼️🎵📹📃",
    "🐶🔎      🖼️🎵📹📃",
]

# Specific default models that the user can download when running installation_linux.sh
DEFAULT_MODELS: list[dict] = [
    {
        "name": "llava",
        "info": {
            "size": 4.7,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/llava",
        },
    },
    {
        "name": "gemma3:12b",
        "info": {
            "size": 8.1,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/gemma3:12b",
        },
    },
    {
        "name": "qwen3.6",
        "info": {
            "size": 22.0,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/qwen3.6",
        },
    },
    {
        "name": "minicpm-v4.6",
        "info": {
            "size": 1.6,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/minicpm-v4.6",
        },
    },
    {
        "name": "llama3.2-vision:11b",
        "info": {
            "size": 7.8,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/llama3.2-vision:11b",
        },
    },
    {
        "name": "moondream",
        "info": {
            "size": 1.7,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/moondream",
        },
    },
    {
        "name": "dima806/deepfake_vs_real_image_detection",
        "info": {
            "size": 3.78,  # GB
            "input": "image",
            "backend": "huggingface",
            "link": "https://huggingface.co/dima806/deepfake_vs_real_image_detection",
        },
    },
    {
        "name": "mo-thecreator/Deepfake-audio-detection",
        "info": {
            "size": 0.379,  # GB
            "input": "audio",
            "backend": "huggingface",
            "link": "https://huggingface.co/mo-thecreator/Deepfake-audio-detection",
        },
    },
    {
        "name": "Hemgg/Deepfake-audio-detection",
        "info": {
            "size": 0.378,  # GB
            "input": "audio",
            "backend": "huggingface",
            "link": "https://huggingface.co/Hemgg/Deepfake-audio-detection",
        },
    },
    {
        "name": "MelodyMachine/Deepfake-audio-detection-V2",
        "info": {
            "size": 0.378,  # GB
            "input": "audio",
            "backend": "huggingface",
            "link": "https://huggingface.co/MelodyMachine/Deepfake-audio-detection-V2",
        },
    },
    {
        "name": "Organika/sdxl-detector",
        "info": {
            "size": 1.74,  # GB
            "input": "image",
            "backend": "huggingface",
            "link": "https://huggingface.co/Organika/sdxl-detector",
        },
    },
    {
        "name": "Vansh180/VideoMae-ffc23-deepfake-detector",
        "info": {
            "size": 0.345,  # GB
            "input": "video",
            "backend": "huggingface",
            "link": "https://huggingface.co/Vansh180/VideoMae-ffc23-deepfake-detector",
        },
    },
    {
        "name": "prithivMLmods/Deep-Fake-Detector-v2-Model",
        "info": {
            "size": 1.37,  # GB
            "input": "image",
            "backend": "huggingface",
            "link": "https://huggingface.co/prithivMLmods/Deep-Fake-Detector-v2-Model",
        },
    },
]
