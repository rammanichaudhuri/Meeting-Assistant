tools = [{
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string"
                    },
                    "attendees": {
                        "type": "array",
                        "items": { "type": "string" }
                    }
                },
                "required": ["title", "date", "attendees"]
            }
        },
        },
    }
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "owner": {
                        "type": "string"
                    },
                    "due_date": {
                        "type": "string"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    }
                },
                "required": ["title", "owner"]
            }
        }
    }
}]