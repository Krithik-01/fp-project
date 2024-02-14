import os
from docx import Document
from PyPDF2 import PdfWriter, PdfReader
from fpdf import FPDF
from PIL import Image
import pytesseract

def convert_docx_to_text(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def convert_pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text() + "\n"
    return text

def convert_image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def convert_files_to_pdf(folder_path, output_pdf_path):
    pdf_writer = FPDF()

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith('.docx'):
            text = convert_docx_to_text(file_path)
            pdf_writer.add_page()
            pdf_writer.set_font("Arial", size=12)
            pdf_writer.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))

        elif file_name.endswith('.pdf'):
            text = convert_pdf_to_text(file_path)
            pdf_writer.add_page()
            pdf_writer.set_font("Arial", size=12)
            pdf_writer.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))

        elif file_name.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
                pdf_writer.add_page()
                pdf_writer.set_font("Arial", size=12)
                pdf_writer.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))

        elif file_name.endswith('.png'):
            text = convert_image_to_text(file_path)
            pdf_writer.add_page()
            pdf_writer.set_font("Arial", size=12)
            pdf_writer.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))

    pdf_writer.output(output_pdf_path)

if __name__ == "__main__":
    input_folder = 'docs'
    output_pdf_path = 'output/combined_output1.pdf'
    convert_files_to_pdf(input_folder, output_pdf_path)
