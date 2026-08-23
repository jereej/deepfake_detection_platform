<img src="deftor_icon.png" width="256">

# DEFTOR (DEepFake deTection platfORm)

Deepfake detection platform (`DEFTOR`) is a Command Line Interface (CLI) application that can be used to run analysis on user-given media (basically whatever the model-at-hand can handle) to check whether they contain AI-generated elements or not. Supports both `ollama` and `huggingface` models (either GGUF models through ollama or "normal" models through `transformers`).

## Quick-start
All you need to do is clone this repository locally and run the following command to get started:
```sh
# Linux system, other platforms to be added
./installation_linux.sh && source .venv/bin/activate
```
The script installs `uv` and `ollama` from the official websites *(if not installed already)*, runs `uv sync` and displays the main help screen `deftor -h`.

## Usage examples
### Analysis
Deftor will differentiate between Ollama and HuggingFace models by the model name. Typically, all HuggingFace models contain the `/` character and if the model name has that, it will treat it as a HuggingFace model. If you want to use a HuggingFace model that does not contain `/`, you need to use the `--backend <ollama|huggingface>` argument.

#### Analyze and print output into CLI
```
deftor analyze path/to/image_or_folder -m llava
```
> Deftor will check whether the input path is a single image or a folder and will analyze every file with an appropriate file extension under that folder. If you have multiple folders under a folder and you wish to analyze those, use the `--subfolders` argument.

#### Analyze and save output into a file
```
deftor analyze path/to/image_folder -m dima806/deepfake_vs_real_image_detection --subfolders -o filename -f json
```
> Deftor will save the analysis into `/current/working/directory/analyses/filename.json`. To save the results into another folder, use the `-d/--destination` argument.

### Model management
#### List all models
```
deftor model list
```

#### Download a model
```
deftor model pull <model_name>
```

#### Delete a model
```
deftor model delete <model_name>
```
