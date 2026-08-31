import tkinter as tk

from converter import open_converter_window
from pdf_merger import open_merger_window
from utils import center_window


def show_frame(frame: tk.Frame, all_frames: list[tk.Frame]) -> None:
    """Hide all frames and display the selected one.

    Args:
        frame: The frame to show.
        all_frames: All frames managed by the main window.
    """
    for f in all_frames:
        f.pack_forget()

    frame.pack(fill=tk.BOTH, expand=True)
    frame.update_idletasks()


root = tk.Tk()
root.title("PDF Utility Tool by Andrzej Zernaczuk")
root.resizable(False, True)
root.minsize(width=1000, height=400)
root.after(10, lambda: center_window(root))

welcome_frame = tk.Frame(root)
welcome_label = tk.Label(
    welcome_frame,
    text="Welcome to the PDF Utility Tool by Andrzej Zernaczuk",
    font=("Arial", 24),
)
welcome_label.pack(pady=(50, 25))
instructions_label = tk.Label(welcome_frame, text="Select an option to begin", font=("Arial", 15))
instructions_label.pack()

converter_frame = tk.Frame(root)
merger_frame = tk.Frame(root)
all_frames = [welcome_frame, converter_frame, merger_frame]
buttons_frame = tk.Frame(root)
buttons_frame.pack(fill=tk.X, padx=10, pady=10)

convert_button = tk.Button(
    buttons_frame,
    text="Convert to PDF",
    command=lambda: show_frame(converter_frame, all_frames),
)
convert_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
merge_button = tk.Button(
    buttons_frame,
    text="Merge PDF files",
    command=lambda: show_frame(merger_frame, all_frames),
)
merge_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

open_converter_window(converter_frame)
open_merger_window(merger_frame)

show_frame(welcome_frame, all_frames)

root.mainloop()
