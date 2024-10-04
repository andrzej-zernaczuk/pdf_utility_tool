import tkinter as tk
from tkinter import filedialog, messagebox

def select_files(listbox: tk.Listbox):
    """Select files and add them to the listbox."""
    file_types = [('All files', '*.*')]
    file_paths = filedialog.askopenfilenames(title='Select Files', filetypes=file_types)
    for path in file_paths:
        listbox.insert(tk.END, path)

    listbox.focus_force()


def remove_all_files(listbox: tk.Listbox):
    """Remove all files files from the listbox."""
    listbox.delete(0, tk.END)


# TODO: Add function for converting files to PDF