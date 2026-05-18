from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Connect Qdrant
client = QdrantClient(
    host="localhost",
    port=6333
)

def init_collection(collection_name: str, vector_size: int):
    """Ensures the collection exists with the correct configuration."""
    if not client.collection_exists(collection_name):
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )
        return True
    return False
