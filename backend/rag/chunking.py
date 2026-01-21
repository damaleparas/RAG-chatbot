from langchain_community.text_splitter import RecursiveCharacterTextSplitter
import json
import os


def create_chunks(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def save_chunks(chunks, file_path):
    with open(output_path, "w") as f:
        json.dump(chunks,f)

if __name__ == "__main__":
    from pdf_to_text import extract_text_from_pdf

    pdf_path = os.path.join("data", "knowlwdge.pdf")
    json_path = os.path.join("data", "chunks.json")

    print(f"Extracting text from {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    print(f"Creating chunks from {pdf_path}")
    chunks = create_chunks(text)
    print(f"Saving chunks to {json_path}")
    save_chunks(chunks, json_path)
    print(f"Chunks saved to {json_path}")
    print("Done!")
    
