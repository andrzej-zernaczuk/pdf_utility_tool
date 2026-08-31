# pdf_utility_tool

Python PDF utility tool.

## Development

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

### Setup

Create the virtual environment, installs dependencies, and sets up pre-commit hooks.

```bash
make init_workspace
```

### Common commands

| Command | Description |
|---|---|
| `make init_workspace` | Create venv, install dependencies, and install hooks |
| `make run` | Start the desktop app |
| `make build` | Build a standalone executable with PyInstaller |
| `make clean_workspace` | Remove venv and pre-commit hooks |

### Optional LLM configuration

Copy `.env` and set `API_PROVIDER`, API keys, and model IDs to enable LLM-based filename suggestions during PDF merge.

## Features

Available functionalities:

* Shared:
- [x] Add selected files.
- [x] Remove selected files.
- [x] Remove all files.
* Merging files:
- [x] Change order of selected files.
- [x] Remove duplicate files if they are present.
- [x] Toggle on/off using LLM API for suggesting merged filename based on file names.
- [x] Merge selected PDF files.
* Converting files to PDF:
- [ ] Convert different file types to pdf
