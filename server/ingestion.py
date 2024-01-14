## Ingesting file and converting same to text.

import fitz
from pdfminer.high_level import extract_text
from PIL import Image as im
from pytesseract import image_to_string

def prepare_page_images(file_path):
    dpi = 300
    zoom = dpi / 72
    doc = fitz.open(file_path)
    magnify = fitz.Matrix(zoom, zoom)
    for idx, page in enumerate(doc):
        pix = page.get_pixmap(matrix=magnify)
        pix.save(f"../assets/mock_input/img-{idx}.png")
    images = [im.open(rf"../assets/mock_input/img-{idx}.png") for idx in range(len(doc))]
    return images

def prepare_text(file_path, extension = ".pdf", data_type = "text"):
    content = ''
    if extension == ".pdf" and data_type == "text":
        content = extract_text(file_path)
    elif extension == ".pdf":
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
        
        page_images = prepare_page_images(file_path)
        content += ''.join([image_to_string(page) for page in page_images])
    elif extension == ".txt":
        content = '\n'.join(open(file_path, 'r').readlines())
    return content