import datetime
import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path

from screeninfo import get_monitors


def default_filename() -> str:
    """Generate a timestamp-based default filename for a merged PDF.

    Returns:
        A filename string in the format ``merged_YYYYMMDD_HHMMSS``.
    """
    return f"merged_{datetime.datetime.now(tz=datetime.UTC).strftime('%Y%m%d_%H%M%S')}"


def open_file_with_default_app(file_path: str | Path) -> None:
    """Open a file with the system's default application.

    Args:
        file_path: Path to the file that should be opened.

    Raises:
        OSError: If the current operating system cannot open the file.
        subprocess.SubprocessError: If the platform open command fails.
    """
    resolved_path = Path(file_path).expanduser().resolve()

    if sys.platform == "darwin":
        subprocess.run(["open", str(resolved_path)], check=True)
        return

    if os.name == "nt":
        os.startfile(resolved_path)  # type: ignore[attr-defined]
        return

    subprocess.run(["xdg-open", str(resolved_path)], check=True)


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
