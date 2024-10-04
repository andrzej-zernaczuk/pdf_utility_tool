import tkinter as tk

from convert_functions import select_files, remove_all_files

def open_converter_window(converter_window: tk.Frame):
    # listbox - space for files list
    listbox = tk.Listbox(converter_window, selectmode=tk.EXTENDED)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # scrollbar for files list
    scrollbar = tk.Scrollbar(converter_window)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # buttons for actions
    select_button = tk.Button(converter_window, text='Select files for converting to PDF', width=25, command=lambda: select_files(listbox))
    select_button.pack(fill=tk.X, padx=10)

    remove_all_button = tk.Button(converter_window, text='Remove all files', command=lambda: remove_all_files(listbox))
    remove_all_button.pack(fill=tk.X, padx=10)