import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

def select_pdfs():
    """Select PDF files and add them to the listbox."""
    file_types = [('PDF files', '*.pdf'), ('All files', '*.*')]
    file_paths = filedialog.askopenfilenames(title='Select PDF Files', filetypes=file_types)
    for path in file_paths:
        listbox.insert(tk.END, path)

# TODO: add persistent selection to the listbox
def move_selected_pdfs_up():
    """Move selected PDF files up in the listbox."""
    selected_indices = listbox.curselection()
    for i in selected_indices:
        if i > 0:
            listbox.insert(i - 1, listbox.get(i))
            listbox.delete(i + 1)

def move_selected_pdfs_down():
    """Move selected PDF files down in the listbox."""
    selected_indices = listbox.curselection()
    for i in reversed(selected_indices):
        if i < listbox.size() - 1:
            listbox.insert(i + 2, listbox.get(i))
            listbox.delete(i)

def remove_selected_pdfs():
    """Remove selected PDF files from the listbox."""
    selected_indices = listbox.curselection()
    for i in reversed(selected_indices):
        listbox.delete(i)

def remove_all_pdfs():
    """Remove all PDF files from the listbox."""
    listbox.delete(0, tk.END)

def merge_pdfs():
    """Merge the selected PDF files into a single PDF file"""
    paths = listbox.get(0, tk.END)
    if not paths:
        messagebox.showwarning('No PDF Files Selected', 'Please select one or more PDF files to merge.')
        return
    if len(paths) == 1:
        messagebox.showwarning('Not Enough PDF Files Selected', 'Please select at least two PDF files to merge.')
        return

    try:
        merger = PyPDF2.PdfMerger()
        for path in paths:
            merger.append(path)

        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_pdf_path:
            return  # User cancelled save

        merger.write(output_pdf_path)
        merger.close()
        messagebox.showinfo('Success', 'The PDF files have been successfully merged!')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

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
select_button = tk.Button(root, text='Select PDF Files', command=select_pdfs)
select_button.pack(fill=tk.X)
# Frame to hold the move buttons
move_buttons_frame = tk.Frame(root)
move_buttons_frame.pack(fill=tk.X)

move_up_button = tk.Button(move_buttons_frame, text='Move Up', command=move_selected_pdfs_up)
move_up_button.pack(side=tk.LEFT ,fill=tk.X, expand=True)
move_down_button = tk.Button(move_buttons_frame, text='Move Down', command=move_selected_pdfs_down)
move_down_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

remove_button = tk.Button(root, text='Remove Selected PDF Files', command=remove_selected_pdfs)
remove_button.pack(fill=tk.X)
remove_all_button = tk.Button(root, text='Remove All PDF Files', command=remove_all_pdfs)
remove_all_button.pack(fill=tk.X)
merge_button = tk.Button(root, text='Merge PDF Files', command=merge_pdfs)
merge_button.pack(fill=tk.X)

root.mainloop()