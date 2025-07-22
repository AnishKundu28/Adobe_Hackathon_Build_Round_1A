import fitz  # PyMuPDF

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_page_elements(self):
        doc = fitz.open(self.pdf_path)
        all_pages = []
        for i, page in enumerate(doc):
            lines = []
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            # filter out non-meaningful
                            span_text = span["text"].strip()
                            if span_text:  # skip blank
                                lines.append({
                                    "text": span_text,
                                    "font": span.get("font", ""),
                                    "size": float(span["size"]),
                                    "page": i + 1
                                })
            all_pages.append(lines)
        return all_pages
