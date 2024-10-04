import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

from utils import generate_suggested_filename

def select_pdfs(listbox: tk.Listbox):
    """Select PDF files and add them to the listbox."""
    file_types: list[tuple] = [('PDF files', '*.pdf'), ('All files', '*.*')]
    file_paths = filedialog.askopenfilenames(title='Select PDF Files', filetypes=file_types)
    current_paths = listbox.get(0, tk.END)
    duplicate_paths: list = [path for path in file_paths if path in current_paths]

    for path in file_paths:
        listbox.insert(tk.END, path)

    if duplicate_paths:
        remove_duplicates_flag: bool = messagebox.askyesno("Duplicate Files", "You have selected duplicate files. Do you want to remove them?", parent=listbox)

        # if user selects YES remove duplicates
        if remove_duplicates_flag:
            remove_duplicates(listbox)

    listbox.focus_force()


def move_selected_pdfs_up(listbox: tk.Listbox):
    """Move selected PDF files up in the listbox."""
    selected_indices = listbox.curselection()

    if any(i == 0 for i in selected_indices):
        messagebox.showerror("Move Error", "Cannot move the first item up.", parent=listbox)
        return

    for i in selected_indices:
        pdf_path = listbox.get(i)
        listbox.delete(i)
        listbox.insert(i - 1, pdf_path)

    listbox.select_clear(0, tk.END)

    for i in selected_indices:
        listbox.select_set(i - 1)


def move_selected_pdfs_down(listbox: tk.Listbox):
    """Move selected PDF files down in the listbox."""
    selected_indices = listbox.curselection()

    if any(i == listbox.size() - 1 for i in selected_indices):
        messagebox.showerror("Move Error", "Cannot move the last item down.", parent=listbox)
        return

    for i in reversed(selected_indices):
        pdf_path = listbox.get(i)
        listbox.delete(i)
        listbox.insert(i + 1, pdf_path)

    listbox.select_clear(0, tk.END)

    for i in selected_indices:
        listbox.select_set(i + 1)


def remove_duplicates(listbox: tk.Listbox):
    """Remove duplicate PDF files from the listbox while preserving order."""
    paths = listbox.get(0, tk.END)
    seen = set()
    new_paths = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            new_paths.append(path)
    listbox.delete(0, tk.END)
    for new_path in new_paths:
        listbox.insert(tk.END, new_path)
    messagebox.showinfo('Success', 'Duplicate PDF files were removed!', parent=listbox)


def update_remove_duplicate_button_state(listbox: tk.Listbox, button: tk.Button):
    """Update the state of the 'Remove Duplicate' button based on listbox content."""
    paths = listbox.get(0, tk.END)
    if len(paths) != len(set(paths)):  # Check if there are any duplicates
        button.config(state='normal')  # Enable the button if duplicates exist
    else:
        button.config(state='disabled')  # Disable the button if no duplicates


def remove_selected_pdfs(listbox: tk.Listbox):
    """Remove selected PDF files from the listbox."""
    selected_indices = listbox.curselection()
    for i in reversed(selected_indices):
        listbox.delete(i)


def remove_all_pdfs(listbox: tk.Listbox):
    """Remove all PDF files from the listbox."""
    listbox.delete(0, tk.END)


def merge_pdfs(listbox: tk.Listbox, suggest_name: bool=False):
    """Merge the selected PDF files into a single PDF file"""
    paths = listbox.get(0, tk.END)
    if not paths:
        messagebox.showwarning('No PDF Files Selected', 'Please select one or more PDF files to merge.', parent=listbox)
        return
    if len(paths) == 1:
        messagebox.showwarning('Not Enough PDF Files Selected', 'Please select at least two PDF files to merge.', parent=listbox)
        return

    # create a list from paths, from every path remove the part before the last slash
    file_names = [path.split('/')[-1] for path in paths]
    # if .pdf is present, remove it
    file_names = [name.replace('.pdf', '') for name in file_names]

    suggested_name: str = generate_suggested_filename(file_names, suggest_name)

    try:
        merger = PyPDF2.PdfMerger()
        for path in paths:
            merger.append(path)

        output_pdf_path = filedialog.asksaveasfilename(
            initialfile=suggested_name,
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            parent=listbox
        )
        if not output_pdf_path:
            return  # User cancelled save

        merger.write(output_pdf_path)
        merger.close()
        messagebox.showinfo('Success', 'The PDF files have been successfully merged!', parent=listbox)
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}', parent=listbox)