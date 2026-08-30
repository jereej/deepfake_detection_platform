<img src="deftor_icon.png" width="256">

# DEFTOR (DEepFake deTection platfORm)

Deepfake detection platform (`DEFTOR`) is a Python Command-Line Interface (CLI) application that can be used to run analysis on user-given media (whatever the model-at-hand can handle, *i.e. text/images/videos/audio*) to check whether they contain AI-generated elements or not.

DEFTOR supports both `Ollama` and `Hugging Face` models. HF models are used through the [transformers](https://huggingface.co/docs/transformers/en/index) framework/library and Ollama models are used through the [Ollama Python Library](https://github.com/ollama/ollama-python).

## Quick-start
All you need to do is clone this repository locally and run the following command to get started:
```sh
./installation_linux.sh && source .venv/bin/activate
```
> Currently only supports Linux systems.

DEFTOR supports downloading some arbitrarily selected Ollama/HF models during the installation process. All supported models are listed below.

| Name | Type | Platform | Size | URL |
| :-- | :--- | :------ | :--- | :-- |
| llava | image | Ollama | 4.7GB | [website](https://ollama.com/library/llava) |
| gemma4 | image | Ollama | 9.6GB | [website](https://ollama.com/library/gemma4) |
| qwen3.8 | image | Ollama | 18.0GB | [website](https://ollama.com/library/qwen3.8) |
| nemotron3:33b | image | Ollama | 28.0GB | [website](https://ollama.com/library/nemotron3) |
| muse-glimmer | image | Ollama | 18.0GB | [website](https://ollama.com/library/muse-glimmer) |
| dima806/deepfake_vs_real_image_detection | image | Hugging Face | 3.78GB | [website](https://huggingface.co/dima806/deepfake_vs_real_image_detection) |
| mo-thecreator/Deepfake-audio-detection | audio | Hugging Face | 0.379GB | [website](https://huggingface.co/mo-thecreator/Deepfake-audio-detection) |
| Hemgg/Deepfake-audio-detection | audio | Hugging Face | 0.378GB | [website](https://huggingface.co/Hemgg/Deepfake-audio-detection) |

## Standard Usage examples
### Analysis
DEFTOR will differentiate between Ollama and Hugging Face models by the model name. Typically, all Hugging Face models contain the `/` character and if the model name has that, it will treat it as a Hugging Face model. If you want to use a Hugging Face model that does not contain `/`, you need to use the `--backend <ollama|huggingface>` argument.

#### Analyze and print output into CLI
```
deftor analyze path/to/image_or_folder -m llava
```
> DEFTOR will check whether the input path is a single image or a folder and will analyze every file with an appropriate file extension under that folder. If you have multiple folders under a folder and you wish to analyze those as well, use the `--subfolders` argument.

#### Analyze and save output into a file
```
deftor analyze path/to/image_folder -m dima806/deepfake_vs_real_image_detection --subfolders -o filename -f json
```
> DEFTOR will save the analysis into `/current/working/directory/analyses/filename.json`. To save the results into another folder, use the `-d/--destination` argument.

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

## Additional usage
Generates a report based on the information found in `statistics.csv` with further information about DEFTOR executions. Saves the report into a `report.md` file.
```
deftor report
```
> NOTE: `statistics.csv` is saved into `current/working/directory/statistics.csv` so you need to run this command from the same directory

## AI-usage disclosure
AI has been used during the development of DEFTOR.

Claude sonnet 5 with Medium effort has been used for the following tasks:
- `src/deftor/lib/reporter.py`
  - Completely generated with AI as it is an additional feature
- `src/deftor/lib/prompter.py`
  - Ideated capturing execution statistics through specific classes for further analysis in `reporter.py`
  - Corrected the `RunStatistics` and `ItemStatistics` classes
  - Corrected `huggingface_prompt()`
- `src/deftor/lib/lib/outputter.py`
  - Fixed `append_execution_stats()`
- Correctly using the `typing` library in `src/deftor/utils/constants.py`
- Deciding on which `pre-commit` hooks to use in `.pre-commit-config.yaml`
- General debugging

OpenAI's GPT-5.6 Luna model was used for:
- Generating the `deftor_icon.png` through the image-generation tool
