from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct
import cohere
import os

try:
    from app.config import COHERE_API_KEY
    from app.qdrant_db import client, init_collection
except ImportError:
    from config import COHERE_API_KEY
    from qdrant_db import client, init_collection

# Initialize Cohere
co = cohere.Client(COHERE_API_KEY)

def process_pdf(file_path: str, collection_name: str = "documents"):
    """Reads PDF (or text fallback), chunks text, embeds, and stores in Qdrant."""
    if not os.path.exists(file_path):
        # If running from app/ directory, check one level up
        if os.path.exists(os.path.join("..", file_path)):
            file_path = os.path.join("..", file_path)
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    text = ""
    try:
        # Try reading as PDF
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    except Exception as pdf_err:
        print(f"PDF parsing failed ({pdf_err}), trying plain text fallback...")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as txt_err:
            raise ValueError(f"Failed to read file as PDF or Text: {txt_err}")

    if not text.strip():
        raise ValueError("No text extracted from file.")

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    # Generate embeddings
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embeddings = response.embeddings
    vector_size = len(embeddings[0])

    # Ensure collection exists
    init_collection(collection_name, vector_size)

    # Store vectors
    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={"text": chunk}
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points
    )

    return f"Processed {len(chunks)} chunks from {file_path}"

if __name__ == "__main__":
    # This allows running the script directly
    try:
        # Check for uploads folder relative to this script
        sample_path = "uploads/sample.pdf"
        print(process_pdf(sample_path))
        print("PDF embedded successfully!")
    except Exception as e:
        print(f"Error: {e}")
