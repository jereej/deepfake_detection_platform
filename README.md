<img src="deftor_icon.png" width="256">

# DEFTOR (DEepFake deTection platfORm)

Deepfake detection platform (`DEFTOR`) is a Command Line Interface (CLI) application that can be used to run analysis on user-given media (basically whatever the model-at-hand can handle) to check whether they contain AI-generated elements or not. Supports both `ollama` and `huggingface` models (either GGUF models through ollama or "normal" models through `transformers`).

## Quick-start
All you need to do is clone this repository locally and run the following command to get started:
```sh
# Linux system, other platforms to be added
./installation_linux.sh && source .venv/bin/activate
```
The script will prompt the user about downloading some default models if the user wishes so. Currently supported default models are:
| Name | Type | Platform | Size | URL |
| :-- | :--- | :------ | :--- | :-- |
| llava | image | Ollama | 4.7GB | https://ollama.com/library/llava |
| gemma4 | image | Ollama | 9.6GB | https://ollama.com/library/gemma4 |
| qwen3.8 | image | Ollama | 18.0GB | https://ollama.com/library/qwen3.8 |
| nemotron3:33b | image | Ollama | 28.0GB | https://ollama.com/library/nemotron3 |
| muse-glimmer | image | Ollama | 18.0GB | https://ollama.com/library/muse-glimmer |
| dima806/deepfake_vs_real_image_detection | image | HuggingFace | 3.78GB | https://huggingface.co/dima806/deepfake_vs_real_image_detection |
| mo-thecreator/Deepfake-audio-detection | audio | HuggingFace | 0.379GB | https://huggingface.co/mo-thecreator/Deepfake-audio-detection |
| Hemgg/Deepfake-audio-detection | audio | HuggingFace | 0.378GB | https://huggingface.co/Hemgg/Deepfake-audio-detection |

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
