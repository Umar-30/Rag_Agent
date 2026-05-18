import cohere
from app.config import COHERE_API_KEY
from app.qdrant_db import client
from app.prompts import RAG_PROMPT

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

async def ask_question(question: str, collection_name: str = "documents"):
    """Embeds question, retrieves context, and generates answer using Cohere."""
    
    # 1. Create query embedding
    query_embedding = co.embed(
        texts=[question],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    # 2. Search Qdrant
    # Using query_points as search is missing in this environment
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=3
    ).points

    # 3. Build context
    context = "\n\n".join([
        result.payload["text"]
        for result in results
    ])

    # 4. Prompt
    prompt = RAG_PROMPT.format(context=context, question=question)

    # 5. Cohere generation
    # Using co.chat for the final response
    response = co.chat(
        message=prompt,
        model="command-a-03-2025"
    )

    return response.text
