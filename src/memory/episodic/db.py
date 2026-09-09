SCHEMA = """CREATE TABLE IF NOT EXISTS meetings (
  meeting_id   INTEGER PRIMARY KEY,
  title    TEXT,
  participants    TEXT,  
  project_tag     TEXT,
  transcript_path     TEXT,                                
  summary     TEXT,
  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS action_items (
  item_id   INTEGER PRIMARY KEY,
  meeting_id INTEGER REFERENCES meetings(meeting_id),
  text    TEXT,
  owner    TEXT,
  due_date    TEXT,
  status TEXT,
  confidence REAL,
  needs_review INTEGER,
  tool_call_status TEXT
);"""