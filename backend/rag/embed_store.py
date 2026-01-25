import time # Added for the pause
import os
import json
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def create_vector_store():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chunks_path = os.path.join(current_dir, "..", "data", "chunks.json")
    store_path = os.path.join(current_dir, "..", "data", "faiss_index")

    if not os.path.exists(chunks_path):
        print("Error: chunks.json not found.")
        return

    with open(chunks_path, 'r') as f:
        chunks = json.load(f)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    print(f"Generating embeddings for {len(chunks)} chunks...")

    # --- BATCH PROCESSING START ---
    batch_size = 5  # Send only 5 chunks at a time
    vector_store = None

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}...")

        if vector_store is None:
            vector_store = FAISS.from_texts(batch, embeddings)
        else:
            # Add new chunks to the existing store
            vector_store.add_texts(batch)
        
        # Pause for 2 seconds between batches to avoid 429 error
        time.sleep(2) 
    # --- BATCH PROCESSING END ---

    vector_store.save_local(store_path)
    print(f"Successfully saved vector store to: {store_path}")

if __name__ == "__main__":
    create_vector_store()