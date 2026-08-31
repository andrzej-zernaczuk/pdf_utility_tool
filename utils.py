import datetime
import os
import tkinter as tk
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq, GroqError
from openai import OpenAI, OpenAIError
from screeninfo import get_monitors

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

_client: Groq | OpenAI | None = None


def _get_llm_client() -> Groq | OpenAI:
    """Return a configured LLM client, initializing it on first use.

    Returns:
        A Groq or OpenAI client based on `API_PROVIDER`.

    Raises:
        ValueError: If `API_PROVIDER` is missing or unsupported.
    """
    global _client
    if _client is not None:
        return _client

    api_provider = os.getenv("API_PROVIDER")
    if api_provider == "GROQ":
        _client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )
    elif api_provider == "OPENAI":
        _client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG"),
            project=os.getenv("OPENAI_PROJECT"),
        )
    else:
        raise ValueError(
            f"Unsupported API_PROVIDER: {api_provider!r}. Expected 'GROQ' or 'OPENAI'."
        )
    return _client


def is_llm_available() -> bool:
    """Return whether LLM filename suggestions are configured.

    Returns:
        True if a supported provider and its API key are set in the environment.
    """
    api_provider = os.getenv("API_PROVIDER")
    if api_provider == "GROQ":
        return bool(os.getenv("GROQ_API_KEY"))
    if api_provider == "OPENAI":
        return bool(os.getenv("OPENAI_API_KEY"))
    return False


def toggle_llm_api(llm_var: tk.BooleanVar) -> None:
    """Log whether the LLM filename suggestion toggle is enabled.

    Args:
        llm_var: Tkinter variable bound to the LLM checkbox.
    """
    if llm_var.get():
        print(f"LLM API enabled: {os.getenv('API_PROVIDER')}")
    else:
        print(f"LLM API disabled: {os.getenv('API_PROVIDER')}")


def generate_suggested_filename(file_names: list[str], suggest_name: bool) -> str:
    """Generate a suggested filename for a merged PDF document based on the input file names.

    Args:
        file_names: Base names of the PDF files being merged.
        suggest_name: Whether to request a name suggestion from the LLM API.

    Returns:
        A suggested filename without the `.pdf` extension.
    """
    suggested_filename = ""
    prompt = (
        f"Based on these PDF file names: {file_names}, respond by suggesting only one "
        "concise filename for a merged PDF document. It must be without any spaces, "
        "new lines etc.. Write nothing more, just the name of the file without the "
        ".pdf extension."
    )

    if suggest_name:
        try:
            client = _get_llm_client()
            api_provider = os.getenv("API_PROVIDER")
            response = client.chat.completions.create(
                model=f"{os.getenv(f'{api_provider}_MODEL_ID')}",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                max_tokens=20,
            )
            content = response.choices[0].message.content
            if content is not None:
                suggested_filename = content.strip()
        except ValueError as e:
            print(f"LLM API is not configured: {e}")
        except (GroqError, OpenAIError) as e:
            print(f"An error occurred while calling the API: {e}")

    if not suggested_filename:
        suggested_filename = (
            f"merged_{datetime.datetime.now(tz=datetime.UTC).strftime('%Y%m%d_%H%M%S')}"
        )

    return suggested_filename


def center_window(window: tk.Tk) -> None:
    """Center a window on the primary monitor.

    Args:
        window: The Tkinter window to center.
    """
    primary_monitor = get_monitors()[0]

    screen_width = primary_monitor.width
    screen_height = primary_monitor.height

    monitor_x = primary_monitor.x
    monitor_y = primary_monitor.y

    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    x = monitor_x + (screen_width // 2) - (window_width // 2)
    y = monitor_y + (screen_height // 2) - (window_height // 2)

    window.geometry(f"+{x}+{y}")
