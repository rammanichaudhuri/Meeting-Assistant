from memory.semantic.semantic_stor import retrieve_relevant_memories

def build_context_block(transcript_text): 
    semantic_hits = retrieve_relevant_memories(transcript_text[:1000], n_results=5)
    episodic_hits = []

    lines = ["Relevant context from past meetings:"]

    for h in semantic_hits: 
        lines.append(f"- [{h}]")