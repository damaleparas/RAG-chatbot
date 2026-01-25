from langchain_text_splitters import RecursiveCharacterTextSplitter
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
    with open(file_path, "w") as f:
        json.dump(chunks,f)

if __name__ == "__main__":
    from pdf_to_text import extract_text_from_pdf
    
    # This finds the directory where chunking.py lives (backend/rag)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # This goes UP one level to 'backend' and then INTO 'data'
    data_dir = os.path.join(current_dir, "..", "data")
    
    # Ensure the data directory actually exists, if not, create it
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    pdf_path = os.path.join(data_dir, "knowledge.pdf")
    json_path = os.path.join(data_dir, "chunks.json")
    
    print(f"Looking for PDF at: {pdf_path}")
    raw_text = extract_text_from_pdf(pdf_path)
    
    if not raw_text.startswith("Error"):
        print("Creating chunks...")
        chunks = create_chunks(raw_text)
        
        print(f"Saving chunks to: {json_path}")
        save_chunks(chunks, json_path)
        print("Done!")
    else:
        print(raw_text)