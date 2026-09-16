import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from utils import default_filename

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

_SYSTEM_PROMPT = (
    "You are a file naming assistant. "
    "Respond with exactly one filename: no spaces, no extension, no explanation."
)

_client: OpenAI | None = None


@dataclass
class LLMConfig:
    """Configuration for an OpenAI-compatible LLM provider.

    Attributes:
        base_url: Optional API base URL override. If None the default OpenAI endpoint is used.
        api_key: API key used for authentication.
        model_id: Model identifier passed to the completions endpoint.
    """

    base_url: str | None
    api_key: str
    model_id: str


def load_config() -> LLMConfig | None:
    """Load LLM configuration from environment variables.

    Reads ``LLM_BASE_URL`` (optional), ``LLM_API_KEY``, and ``LLM_MODEL_ID``.

    Returns:
        An LLMConfig when all required variables are present, otherwise None.
    """
    api_key = os.getenv("LLM_API_KEY")
    model_id = os.getenv("LLM_MODEL_ID")
    if not api_key or not model_id:
        return None
    return LLMConfig(
        base_url=os.getenv("LLM_BASE_URL") or None,
        api_key=api_key,
        model_id=model_id,
    )


def is_available() -> bool:
    """Return whether LLM filename suggestions are configured.

    Returns:
        True if ``LLM_API_KEY`` and ``LLM_MODEL_ID`` are set in the environment.
    """
    return load_config() is not None


def _get_client() -> OpenAI:
    """Return a cached OpenAI-compatible client, initialising it on first call.

    Returns:
        A configured OpenAI client instance.

    Raises:
        ValueError: If the required environment variables are not set.
    """
    global _client
    if _client is not None:
        return _client
    config = load_config()
    if config is None:
        raise ValueError("LLM is not configured. Set LLM_API_KEY and LLM_MODEL_ID.")
    _client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    return _client


def suggest_filename(file_names: list[str]) -> str:
    """Suggest a merged PDF filename using the configured LLM.

    Sends a request to the configured OpenAI-compatible endpoint. Falls back to
    a timestamp-based name if the LLM is unavailable or the call fails.

    Args:
        file_names: Stem names (without extension) of the PDF files being merged.

    Returns:
        A suggested filename without the ``.pdf`` extension.
    """
    config = load_config()
    if config is None:
        return default_filename()

    prompt = (
        f"Suggest a concise merged PDF filename for these source files: {file_names}. "
        "No spaces, no extension."
    )

    try:
        response = _get_client().chat.completions.create(
            model=config.model_id,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=20,
            timeout=10,
        )
        content = response.choices[0].message.content
        if content:
            return content.strip()
    except OpenAIError as e:
        print(f"LLM API error: {e}")

    return default_filename()
