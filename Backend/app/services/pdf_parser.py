import os
from typing import Dict

import pdfplumber
import pytesseract
from pdf2image import convert_from_path


class PDFParser:
    """
    Extracts text from both digital PDFs and scanned PDFs.
    """

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        text = ""

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"PDF Error: {e}")

        # If no text found, use OCR
        if not text.strip():
            try:
                images = convert_from_path(pdf_path)

                for image in images:
                    text += pytesseract.image_to_string(image)

            except Exception as e:
                print(f"OCR Error: {e}")

        return text


if __name__ == "__main__":

    parser = PDFParser()

    result = parser.extract_text("uploads/report.pdf")

    print(result)