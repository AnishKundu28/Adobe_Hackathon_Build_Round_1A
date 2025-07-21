import os
from extractor import PDFExtractor
from heading_detector import detect_headings
from title_detector import detect_title
from utils import save_json

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_pdf(pdf_path, pdf_name):
    extractor = PDFExtractor(pdf_path)
    pages_data = extractor.extract_page_elements()
    title = detect_title(pages_data)
    outline = detect_headings(pages_data)
    output = {"title": title, "outline": outline}
    output_name = os.path.splitext(pdf_name)[0] + ".json"
    save_json(output, os.path.join(OUTPUT_DIR, output_name))

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in os.listdir(INPUT_DIR):
        if fname.lower().endswith(".pdf"):
            process_pdf(os.path.join(INPUT_DIR, fname), fname)
