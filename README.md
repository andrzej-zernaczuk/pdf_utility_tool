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

Copy `.env.example` to `.env` and fill in the three variables to enable AI-powered filename suggestions during PDF merge.

```
LLM_BASE_URL=https://api.groq.com/openai/v1   # any OpenAI-compatible endpoint
LLM_API_KEY=your-api-key-here
LLM_MODEL_ID=gemma2-9b-it
```

Any OpenAI-compatible provider works — Groq, OpenAI, Ollama (local), vLLM, Together AI, etc. Omit `LLM_BASE_URL` to use the default OpenAI endpoint. LLM suggestions are silently disabled when the variables are not set.

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
