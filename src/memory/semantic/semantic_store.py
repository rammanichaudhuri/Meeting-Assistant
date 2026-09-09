import chromadb
from embedding_pipeline import embed_text
import uuid

client = chromadb.PersistentClient(path="memory/semantic/")
collection = client.get_or_create_collection("facts")

SIMILARITY_THRESHOLD = 0.15

def add_or_update_fact(query: str, fact_text, fact_id, confidence, source_meeting_id) -> str: 
    """should store, store"""

    embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1
    )
    
    if not results["distances"][0]:
        return True
    
    similarity = 1 - results["distances"][0][0]

    if (similarity < 1 - SIMILARITY_THRESHOLD):
    old_id = results["ids"][0][0]
    old_meta = collection.get(ids=[old_id])["metadatas"][0]
    old_meta["superseded"] = True
    collection.update(ids=[old_id], metadatas=[old_meta])

    fact_id = str(uuid.uuid4())

    collection.add(
    documents=[fact_text],
    ids=[fact_id],
    embeddings=[embedding]
    metadatas=[{
        "source_meeting_id": source_meeting_id,
        "confidence": confidence,
        "superseded": False
    }])

    return fact_id

# def extract_memory(conversation_turn: str, llm) -> str:
#     prompt = f"""Extract the key factual information, preferences, or decisions from this interaction that would be useful to remember in future sessions. Be concise — one to three sentences maximum.

#     Interaction: {conversation_turn}

#     Memory:"""
#     return llm.complete(prompt)


def retrieve_relevant_memories(
    query: str,
    collection,
    n_results: int = 5,
    min_relevance_threshold: float = 0.7
    ) -> list[str]:
    
    embedding = embed_text(query)
    
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results * 2,
        include=["documents", "distances"],
        where={"superseded": False}
    )
    
    # Filter by relevance threshold
    memories = []
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        # ChromaDB returns L2 distance; lower is more similar
        similarity = 1 - distance
        if similarity >= min_relevance_threshold:
            memories.append(doc)
    
    return memories