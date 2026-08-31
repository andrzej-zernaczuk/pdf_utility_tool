.PHONY: help init_workspace uv_venv uv_sync hooks_install \
		check lint format format_check typecheck hooks_run \
		run build \
		clean_workspace hooks_uninstall remove_venv delete_build_artifacts

UV := uv
APP := main.py
APP_NAME := pdf-utility-tool

help: ## Show available targets
	@grep -E '^[a-zA-Z_]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'


# Workspace setup
init_workspace: uv_venv uv_sync hooks_install ## Create venv, install dependencies, and set up pre-commit hooks

uv_venv: ## Create project virtual environment with uv
	$(UV) venv

uv_sync: ## Install project dependencies with uv
	$(UV) sync

hooks_install: ## Install pre-commit git hooks
	$(UV) run pre-commit install


# Linting and formatting
check: lint format_check typecheck ## Run all quality checks

lint: ## Run ruff linter
	$(UV) run ruff check .

format: ## Format code with ruff
	$(UV) run ruff format .

format_check: ## Check code formatting with ruff
	$(UV) run ruff format --check .

typecheck: ## Run mypy type checker
	$(UV) run mypy .

hooks_run: ## Run pre-commit on all files
	$(UV) run pre-commit run --all-files


# Running the application
run: ## Run the desktop app
	$(UV) run python $(APP)

build: ## Build standalone executable with PyInstaller
	$(UV) run pyinstaller $(APP) --onefile --windowed --name $(APP_NAME) --clean -y


# Cleanup
clean_workspace: hooks_uninstall clean_venv ## Remove venv and pre-commit hooks

hooks_uninstall: ## Remove pre-commit git hooks
	-$(UV) run pre-commit uninstall

remove_venv: ## Remove project virtual environment
	rm -rf .venv

delete_build_artifacts: ## Remove PyInstaller build artifacts
	rm -rf build dist
	rm -f *.spec