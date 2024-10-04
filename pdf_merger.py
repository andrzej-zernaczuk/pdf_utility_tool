import tkinter as tk
from tkinter import BooleanVar

from utils import toggle_llm_api
from merge_functions import select_pdfs, move_selected_pdfs_up, move_selected_pdfs_down, remove_duplicates, update_remove_duplicate_button_state, remove_selected_pdfs, remove_all_pdfs, merge_pdfs


# Function to open the merger window
def open_merger_window(merger_window: tk.Frame):
    # listbox - space for files list
    listbox = tk.Listbox(merger_window, selectmode=tk.EXTENDED)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # scrollbar for files list
    scrollbar = tk.Scrollbar(merger_window)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # select files for merging
    select_button = tk.Button(merger_window, text='Select PDF files', width=25, command=lambda: [select_pdfs(listbox), update_remove_duplicate_button_state(listbox, remove_duplicate_button)])
    select_button.pack(fill=tk.X, padx=10)

    # frane for move buttons so they are next to each other
    move_buttons_frame = tk.Frame(merger_window)
    move_buttons_frame.pack(fill=tk.X, padx=10)

    # move up selected files
    move_up_button = tk.Button(move_buttons_frame, text='Move up', command=lambda: move_selected_pdfs_up(listbox))
    move_up_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # move down selected files
    move_down_button = tk.Button(move_buttons_frame, text='Move down', command=lambda: move_selected_pdfs_down(listbox))
    move_down_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # remove duplicate files
    remove_duplicate_button = tk.Button(merger_window, text='Remove duplicate PDF files', command=lambda: [remove_duplicates(listbox), remove_duplicate_button.config(state='disabled')])
    remove_duplicate_button.pack(fill=tk.X, padx=10)
    remove_duplicate_button.config(state='disabled') # Default state is disabled - no files to check

    # remove selected files
    remove_button = tk.Button(merger_window, text='Remove selected PDF files', command=lambda: [remove_selected_pdfs(listbox), update_remove_duplicate_button_state(listbox, remove_duplicate_button)])
    remove_button.pack(fill=tk.X, padx=10)

    # remove all files
    remove_all_button = tk.Button(merger_window, text='Remove all PDF files', command=lambda: [remove_all_pdfs(listbox), remove_duplicate_button.config(state='disabled')])
    remove_all_button.pack(fill=tk.X, padx=10)

    # merge PDF files
    merge_button = tk.Button(merger_window, text='Merge PDF files', command=lambda: merge_pdfs(listbox, llm_var.get()))
    merge_button.pack(fill=tk.X, padx=10)

    # LLM API Switch
    global llm_var
    llm_var = BooleanVar(value=False) # Default value is False
    llm_switch = tk.Checkbutton(merger_window, text="Use LLM for suggesting file name", variable=llm_var, command=toggle_llm_api(llm_var))
    llm_switch.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)