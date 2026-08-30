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
    echo "Ollama installation failed. Please check https://ollama.com/download/linux on how to install Ollama by yourself."
    exit 1
fi
echo "'uv' and 'Ollama' found from the system. Proceeding."
# Starts the Ollama server if it does not exist, quickly errors if it does.
# Piping the output to /dev/null and moving to the background so it does not block anything
echo "Starting the local Ollama server if not running already."
ollama serve &> /dev/null &
uv sync
# Asks whether the user wants to install default models
uv run default_model_installation.py
echo "Installation script finished."
uv run deftor -h
