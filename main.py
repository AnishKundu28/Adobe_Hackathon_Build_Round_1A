#!/usr/bin/env python3
import os
import json
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Any

class PDFOutlineExtractor:
    def __init__(self):
        self.input_dir = "/app/input"
        self.output_dir = "/app/output"
        
    def extract_outline(self, file_path: str) -> Dict[str, Any]:
        """Extract outline from a PDF file."""
        doc = fitz.open(file_path)
        outline = []
        
        # Get the document title (use filename if no title metadata)
        title = doc.metadata.get("title", "").strip()
        if not title:
            title = Path(file_path).stem.replace("_", " ").title()
        
        # Extract headings from the document
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks = page.get_text("dict", flags=11)["blocks"]  # flags=11: TEXT_PRESERVE_LIGATURES | TEXT_MEDIABOX_CLIP
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                                
                            # Determine heading level based on font size and style
                            font_size = span["size"]
                            is_bold = "bold" in span["font"].lower()
                            
                            # Simple heuristic for heading detection
                            # This can be enhanced based on your specific PDFs
                            if font_size >= 20 and is_bold:
                                level = "H1"
                            elif font_size >= 16 and is_bold:
                                level = "H2"
                            elif font_size >= 14 and is_bold:
                                level = "H3"
                            else:
                                continue
                                
                            outline.append({
                                "level": level,
                                "text": text,
                                "page": page_num + 1  # 1-based page numbering
                            })
        
        # Try to get outline/toc if available
        toc = doc.get_toc()
        if toc and len(toc) > len(outline):
            outline = []
            for item in toc:
                level, text, page = item[0], item[1], item[2]
                outline.append({
                    "level": f"H{min(level, 3)}",  # Limit to H3 max
                    "text": text.strip(),
                    "page": page
                })
        
        return {
            "title": title,
            "outline": outline
        }
    
    def process_pdfs(self):
        """Process all PDFs in the input directory."""
        input_path = Path(self.input_dir)
        output_path = Path(self.output_dir)
        
        # Ensure output directory exists
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Process each PDF file
        for pdf_file in input_path.glob("*.pdf"):
            try:
                print(f"Processing {pdf_file.name}...")
                result = self.extract_outline(str(pdf_file))
                
                # Save the result as JSON
                output_file = output_path / f"{pdf_file.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"Successfully processed {pdf_file.name}")
                
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {str(e)}")

if __name__ == "__main__":
    extractor = PDFOutlineExtractor()
    extractor.process_pdfs()
