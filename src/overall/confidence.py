
# rule based confidence

def compute_heuristic_confidence(item, transcript):
    score = 1.0
    if not item.get("owner") or item["owner"].lower() in ['someone', 'tbd']:
        score -= 0.4
    if not item.get("due_date"):
        score -= 0.2
    if item["task"].lower() not in transcript.lower():
        score -= 0.2
        
    return max(score, 0.0)