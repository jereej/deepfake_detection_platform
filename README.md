# DEFTOR (DEepFake deTection platfORm)

<img src="deftor_icon.png" width="256">

Deepfake detection platform (`DEFTOR`) is a Command Line Interface (CLI) application that can be used to run analysis on images to check whether they contain AI-generated elements or not.

## Quick-start
All you need to do is run the following command to get started:
```sh
# Linux system, other platforms to be added
./installation_linux.sh && source .venv/bin/activate
```
The script installs `uv` from the official website *(if not installed already)*, runs `uv sync` and displays the main help screen `deftor -h`.

### `deftor -h`
```
usage: deftor [-h] {analyze,model} ...

positional arguments:
  {analyze,model}
    analyze        Analyze an image or folder
    model          Model management

options:
  -h, --help       show this help message and exit
```

### `deftor analyze -h`
```
usage: deftor analyze [-h] -m MODEL [-o OUTPUT] [-f {json,yaml,yml,csv,txt}] [-t TARGET] [--no-timestamp] [--raw] input

positional arguments:
  input                 Path to an image or a folder or images

options:
  -h, --help            show this help message and exit
  -m, --model MODEL     Name of the used model (f.ex. llava or llava:latest)
  -o, --output OUTPUT   Output filename without file extension. Without this parameter, output is directed to stdout. Also includes a timestamp in the YYYYMMDDHHMMSS format
  -f, --format {json,yaml,yml,csv,txt}
                        Output format (default is txt)
  -t, --target TARGET   Target folder of the analysis
  --no-timestamp        Used with -o, if you want to write the file name without the timestamp
  --raw                 If you want the raw LLM analysis output piped to stdout
```

### `deftor model -h`
```
usage: deftor model [-h] {pull,delete,list} ...

positional arguments:
  {pull,delete,list}
    pull              Download a model
    delete            Delete a model
    list              List all locally available models

options:
  -h, --help          show this help message and exit
```