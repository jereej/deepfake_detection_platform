#! /bin/bash

# Install uv if not found
if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found, installing"
    # official installation link from the official uv website
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Exit if uv installation did not work
if ! command -v uv >/dev/null 2>&1; then
    echo "ERROR: uv installation failed or is not in PATH."
    echo "Please check the official uv installation page: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found, installing it"
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Ollama installation did not work
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found, installing it"
    exit 1
fi

echo "'uv' and 'Ollama' found from the system. Proceeding."
uv sync
uv run deftor -h
