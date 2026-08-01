#! /bin/bash

if ! command -v uv &> /dev/null; then
    echo "uv not found, installing"
    # official installation link from the official uv website
    curl -LsSf https://astral.sh/uv/install.sh | sh

    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v uv &> /dev/null; then
        echo "Error: uv installation failed or not found in PATH."
        exit 1
    fi
fi

cd deftor
echo "Running 'uv sync'"
uv sync
echo "Displaying the help page of the deftor application"
uv run deftor -h
