

def create_calendar_event(title, date, attendees=None):
    print(f"[Calendar] Created event {title} on {date}")
    return { "status": "created", "title": title, "date": date }