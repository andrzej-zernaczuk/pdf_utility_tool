import tkinter as tk

from pdf_functions import select_pdfs, move_selected_pdfs_up, move_selected_pdfs_down, remove_selected_pdfs, remove_all_pdfs, merge_pdfs

# main window
root = tk.Tk()
root.title("PDF Merger by Andrzej Zernaczuk")
root.geometry("800x600")

# listbox - space for files list
listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# scrollbar for files list
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# buttons for actions
select_button = tk.Button(root, text='Select PDF Files', command=lambda: select_pdfs(listbox))
select_button.pack(fill=tk.X)

# Frame to hold the move buttons
move_buttons_frame = tk.Frame(root)
move_buttons_frame.pack(fill=tk.X)

move_up_button = tk.Button(move_buttons_frame, text='Move Up', command=lambda: move_selected_pdfs_up(listbox))
move_up_button.pack(side=tk.LEFT ,fill=tk.X, expand=True)
move_down_button = tk.Button(move_buttons_frame, text='Move Down', command=lambda: move_selected_pdfs_down(listbox))
move_down_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

remove_button = tk.Button(root, text='Remove Selected PDF Files', command=lambda: remove_selected_pdfs(listbox))
remove_button.pack(fill=tk.X)
remove_all_button = tk.Button(root, text='Remove All PDF Files', command=lambda: remove_all_pdfs(listbox))
remove_all_button.pack(fill=tk.X)
merge_button = tk.Button(root, text='Merge PDF Files', command=lambda: merge_pdfs(listbox))
merge_button.pack(fill=tk.X)

root.mainloop()