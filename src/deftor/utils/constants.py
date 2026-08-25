# Constants that are used in various parts of DEFTOR
from typing import Literal

# Media type extensions map
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
DEFAULT_PROMPT = """DEEPFAKE / AI-GENERATED IMAGE DETECTION

Analyze the given image for evidence of AI generation.

Provide:
- classification
- evidence: 2-4 concise, specific, observable details

Do not explain your reasoning outside these fields."""

# Default options for Ollama models
DEFAULT_OPTIONS = {"num_predict": 2048}

# ... syntax allows >=1 items in a tuple
FAKE_KEYWORDS: tuple[str, ...] = ("fake", "deepfake", "synthetic", "generated", "spoof", "ai")

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
# The model sizes are taken from the websites below
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
        "name": "gemma4",
        "info": {
            "size": 9.6,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/gemma4",
        },
    },
    {
        "name": "qwen3.8",
        "info": {
            "size": 18.0,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/qwen3.8",
        },
    },
    {
        "name": "nemotron3:33b",
        "info": {
            "size": 28.0,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/nemotron3",
        },
    },
    {
        "name": "muse-glimmer",
        "info": {
            "size": 18.0,  # GB
            "input": "image",
            "backend": "ollama",
            "link": "https://ollama.com/library/muse-glimmer",
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
]
