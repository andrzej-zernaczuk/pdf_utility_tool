import tkinter as tk
from tkinter import BooleanVar

from merge_functions import (
    merge_pdfs,
    move_selected_pdfs_down,
    move_selected_pdfs_up,
    remove_all_pdfs,
    remove_duplicates,
    remove_selected_pdfs,
    select_pdfs,
    update_remove_duplicate_button_state,
)
from utils import is_llm_available, toggle_llm_api


def open_merger_window(merger_window: tk.Frame) -> None:
    """Build and populate the PDF merger UI inside the given frame.

    Args:
        merger_window: The parent frame for merger widgets.
    """
    # listbox - space for files list
    listbox = tk.Listbox(merger_window, selectmode=tk.EXTENDED)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # scrollbar for files list
    scrollbar = tk.Scrollbar(merger_window)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    remove_duplicate_button = tk.Button(merger_window, text='Remove duplicate PDF files')
    remove_duplicate_button.pack(fill=tk.X, padx=10)
    remove_duplicate_button.config(state='disabled')

    def on_select_pdfs() -> None:
        select_pdfs(listbox)
        update_remove_duplicate_button_state(listbox, remove_duplicate_button)

    def on_remove_duplicates() -> None:
        remove_duplicates(listbox)
        remove_duplicate_button.config(state='disabled')

    def on_remove_selected() -> None:
        remove_selected_pdfs(listbox)
        update_remove_duplicate_button_state(listbox, remove_duplicate_button)

    def on_remove_all() -> None:
        remove_all_pdfs(listbox)
        remove_duplicate_button.config(state='disabled')

    select_button = tk.Button(
        merger_window, text='Select PDF files', width=25, command=on_select_pdfs,
    )
    select_button.pack(fill=tk.X, padx=10)

    move_buttons_frame = tk.Frame(merger_window)
    move_buttons_frame.pack(fill=tk.X, padx=10)

    move_up_button = tk.Button(
        move_buttons_frame, text='Move up', command=lambda: move_selected_pdfs_up(listbox),
    )
    move_up_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    move_down_button = tk.Button(
        move_buttons_frame, text='Move down', command=lambda: move_selected_pdfs_down(listbox),
    )
    move_down_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    remove_duplicate_button.config(command=on_remove_duplicates)

    remove_button = tk.Button(
        merger_window, text='Remove selected PDF files', command=on_remove_selected,
    )
    remove_button.pack(fill=tk.X, padx=10)

    remove_all_button = tk.Button(
        merger_window, text='Remove all PDF files', command=on_remove_all,
    )
    remove_all_button.pack(fill=tk.X, padx=10)

    llm_var = BooleanVar(value=False)
    merge_button = tk.Button(merger_window, text='Merge PDF files', command=lambda: merge_pdfs(listbox, llm_var.get()))
    merge_button.pack(fill=tk.X, padx=10)

    llm_switch = tk.Checkbutton(
        merger_window,
        text="Use LLM to suggest file name",
        variable=llm_var,
        command=lambda: toggle_llm_api(llm_var),
    )
    if not is_llm_available():
        llm_switch.config(state="disabled")
    llm_switch.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)