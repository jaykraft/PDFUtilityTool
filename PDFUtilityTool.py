import PyPDF2
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, Text
from tkinter import ttk


# Function Definitions
def merge_pdfs(pdf_list, output):
    """
    Merge multiple PDF files into a single file.
    - pdf_list: List of PDF file paths to merge.
    - output: Output file name for the merged PDF.
    """
    try:
        merger = PyPDF2.PdfMerger()
        for pdf in pdf_list:
            merger.append(pdf)
        if not output.endswith('.pdf'):
            output += '.pdf'
        with open(output, 'wb') as f:
            merger.write(f)
        messagebox.showinfo("Success", f"Merged PDFs saved as {output}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")


def split_pdf(input_pdf, output_dir):
    """
    Split a single PDF into individual pages.
    - input_pdf: Path to the PDF file to split.
    - output_dir: Directory to save split pages.
    """
    try:
        with open(input_pdf, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for i in range(len(reader.pages)):
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[i])
                output_path = os.path.join(output_dir, f'page_{i + 1}.pdf')
                with open(output_path, 'wb') as out:
                    writer.write(out)
        messagebox.showinfo("Success", f"Pages saved in {output_dir}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to split PDF: {e}")


def password_protect(input_pdf, output_pdf, password):
    """
    Password protect a PDF file.
    - input_pdf: Path to the PDF file to protect.
    - output_pdf: Path to save the protected PDF.
    - password: Password for the PDF.
    """
    try:
        with open(input_pdf, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)
            if not output_pdf.endswith('.pdf'):
                output_pdf += '.pdf'
            with open(output_pdf, 'wb') as f:
                writer.write(f)
        messagebox.showinfo("Success", f"PDF protected and saved as {output_pdf}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to protect PDF: {e}")


# Helper Functions for UI
def open_file(entry):
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)


def open_files(entry):
    filepaths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if filepaths:
        entry.delete(0, tk.END)
        entry.insert(0, ", ".join(filepaths))


def select_folder(entry):
    folderpath = filedialog.askdirectory()
    if folderpath:
        entry.delete(0, tk.END)
        entry.insert(0, folderpath)


def set_tooltip(widget, text):
    tooltip = ttk.Label(widget, text=text, relief="solid", background="yellow")

    def show_tooltip(event):
        tooltip.place(x=event.x_root - widget.winfo_rootx(), y=event.y_root - widget.winfo_rooty())

    def hide_tooltip(event):
        tooltip.place_forget()

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)


# Main UI
def main():
    root = tk.Tk()
    root.title("PDF Utility Tool")
    root.geometry("800x800")

    def show_main_menu():
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="PDF Utility Tool", font=("Arial", 16)).pack(pady=10)

        merge_button = tk.Button(root, text="Merge PDFs", command=show_merge_ui)
        merge_button.pack(pady=5)
        set_tooltip(merge_button, "Merge multiple PDF files into one.")

        split_button = tk.Button(root, text="Split PDF", command=show_split_ui)
        split_button.pack(pady=5)
        set_tooltip(split_button, "Split a PDF into individual pages.")

        protect_button = tk.Button(root, text="Password Protect PDF", command=show_protect_ui)
        protect_button.pack(pady=5)
        set_tooltip(protect_button, "Add a password to a PDF file.")

    def show_merge_ui():
        def merge_action():
            pdfs = input_pdfs.get().split(', ')
            output = output_file.get()
            if pdfs and output:
                merge_pdfs(pdfs, output)
            else:
                messagebox.showerror("Error", "Please provide all required inputs.")

        for widget in root.winfo_children():
            widget.destroy()

        tk.Button(root, text="Back", command=show_main_menu).pack(anchor="nw")

        tk.Label(root, text="Select PDF files to merge:").pack()
        input_pdfs = tk.Entry(root, width=50)
        input_pdfs.pack()
        tk.Button(root, text="Browse Files", command=lambda: open_files(input_pdfs)).pack()

        tk.Label(root, text="Output file name:").pack()
        output_file = tk.Entry(root, width=50)
        output_file.pack()

        tk.Button(root, text="Merge PDFs", command=merge_action).pack()

    def show_split_ui():
        def split_action():
            input_pdf = input_file.get()
            output_dir = output_folder.get()
            if input_pdf and output_dir:
                split_pdf(input_pdf, output_dir)
            else:
                messagebox.showerror("Error", "Please provide all required inputs.")

        for widget in root.winfo_children():
            widget.destroy()

        tk.Button(root, text="Back", command=show_main_menu).pack(anchor="nw")

        tk.Label(root, text="Select a PDF file to split:").pack()
        input_file = tk.Entry(root, width=50)
        input_file.pack()
        tk.Button(root, text="Browse File", command=lambda: open_file(input_file)).pack()

        tk.Label(root, text="Select output directory:").pack()
        output_folder = tk.Entry(root, width=50)
        output_folder.pack()
        tk.Button(root, text="Select Folder", command=lambda: select_folder(output_folder)).pack()

        tk.Button(root, text="Split PDF", command=split_action).pack()

    def show_protect_ui():
        def protect_action():
            input_pdf = input_file.get()
            output_pdf = output_file.get()
            password = password_entry.get()
            if input_pdf and output_pdf and password:
                password_protect(input_pdf, output_pdf, password)
            else:
                messagebox.showerror("Error", "Please provide all required inputs.")

        for widget in root.winfo_children():
            widget.destroy()

        tk.Button(root, text="Back", command=show_main_menu).pack(anchor="nw")

        tk.Label(root, text="Select a PDF file to protect:").pack()
        input_file = tk.Entry(root, width=50)
        input_file.pack()
        tk.Button(root, text="Browse File", command=lambda: open_file(input_file)).pack()

        tk.Label(root, text="Output file name:").pack()
        output_file = tk.Entry(root, width=50)
        output_file.pack()

        tk.Label(root, text="Enter password:").pack()
        password_entry = tk.Entry(root, width=50, show='*')
        password_entry.pack()

        tk.Button(root, text="Protect PDF", command=protect_action).pack()

    show_main_menu()
    root.mainloop()


if __name__ == "__main__":
    main()
