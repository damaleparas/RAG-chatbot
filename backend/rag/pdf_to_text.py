from pypdf import PdfReader
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        return "no file found"

    reader = PdfReader(pdf_path)
    raw_text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text

if __name__ == "__main__":
    path = os.path.join("data", "knowlwdge.pdf")
    text = extract_text_from_pdf(path)
    print(f"Extracted {len(text)} characters from {path}")