import tkinter as tk

from convert_functions import remove_all_files, select_files


def open_converter_window(converter_window: tk.Frame) -> None:
    """Build and populate the file converter UI inside the given frame.

    Args:
        converter_window: The parent frame for converter widgets.
    """
    listbox = tk.Listbox(converter_window, selectmode=tk.EXTENDED)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(converter_window)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    select_button = tk.Button(
        converter_window,
        text='Select files for converting to PDF',
        width=25,
        command=lambda: select_files(listbox),
    )
    select_button.pack(fill=tk.X, padx=10)

    remove_all_button = tk.Button(
        converter_window,
        text='Remove all files',
        command=lambda: remove_all_files(listbox),
    )
    remove_all_button.pack(fill=tk.X, padx=10)
