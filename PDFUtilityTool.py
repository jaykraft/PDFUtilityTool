import PyPDF2
import os
from pathlib import Path

def merge_pdfs(pdf_list, output):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    with open(output, 'wb') as f:
        merger.write(f)
    print(f'Merged PDFs saved as {output}')

def split_pdf(input_pdf, output_dir):
    with open(input_pdf, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for i in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            output_path = os.path.join(output_dir, f'page_{i + 1}.pdf')
            with open(output_path, 'wb') as out:
                writer.write(out)
            print(f'Page {i + 1} saved as {output_path}')

def password_protect(input_pdf, output_pdf, password):
    with open(input_pdf, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        with open(output_pdf, 'wb') as f:
            writer.write(f)
        print(f'PDF protected and saved as {output_pdf}')

def main():
    print("PDF Utility Tool")
    print("1. Merge PDFs")
    print("2. Split PDF")
    print("3. Password Protect PDF")
    choice = input("Choose an option (1/2/3): ")

    if choice == '1':
        pdfs = input("Enter PDF file paths to merge (comma separated): ").split(',')
        output = input("Enter output file name: ")
        merge_pdfs([Path(pdf.strip()) for pdf in pdfs], output)

    elif choice == '2':
        input_pdf = input("Enter PDF file to split: ")
        output_dir = input("Enter directory to save split pages: ")
        split_pdf(input_pdf, output_dir)

    elif choice == '3':
        input_pdf = input("Enter PDF file to protect: ")
        output_pdf = input("Enter output file name: ")
        password = input("Enter password: ")
        password_protect(input_pdf, output_pdf, password)

    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()