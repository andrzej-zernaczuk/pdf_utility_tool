import tkinter as tk

from pdf_merger import open_merger_window
from converter import open_converter_window
from utils import center_window


def show_frame(frame, all_frames):
    # Hide all frames
    for f in all_frames:
        f.pack_forget()

    # Show the selected frame
    frame.pack(fill=tk.BOTH, expand=True)

    # Force an update to ensure all widgets are properly displayed
    frame.update_idletasks()

# main window
root = tk.Tk()
root.title("PDF Utility Tool by Andrzej Zernaczuk")
root.resizable(False, True)  # Disable resizing in both width and height
root.minsize(width=1000, height=400)
root.after(10, lambda: center_window(root))

# Create a frame for the welcome screen
welcome_frame = tk.Frame(root)
welcome_label = tk.Label(welcome_frame, text="Welcome to the PDF Utility Tool by Andrzej Zernaczuk", font=("Arial", 24))
welcome_label.pack(pady=(50, 25))
instructions_label = tk.Label(welcome_frame, text="Select an option to begin", font=("Arial", 15))
instructions_label.pack()

# Create a frame for each section (Converter, Merger)
converter_frame = tk.Frame(root)
merger_frame = tk.Frame(root)
all_frames = [welcome_frame, converter_frame, merger_frame]
buttons_frame = tk.Frame(root)
buttons_frame.pack(fill=tk.X, padx=10, pady=10)

# Create buttons to switch between frames
convert_button = tk.Button(buttons_frame, text="Convert to PDF", command=lambda: show_frame(converter_frame, all_frames))
convert_button.pack(side=tk.LEFT ,fill=tk.X, expand=True)
merge_button = tk.Button(buttons_frame, text="Merge PDF files", command=lambda: show_frame(merger_frame, all_frames))
merge_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))


# Add content to the Converter and Merger frame
open_converter_window(converter_frame)
open_merger_window(merger_frame)

# Initially, show the welcome frame
show_frame(welcome_frame, all_frames)

root.mainloop()