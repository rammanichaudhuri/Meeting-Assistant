

def create_task(title, owner, due_date=None, priority="medium"):
    print(f"[Task] Created task '{title}' for {owner} (priority: {priority})")
    return { "status": "created", "title": title }