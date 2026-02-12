import json
from datetime import datetime

def log(endpoint, status, message, data=None):
    log_entry = {
        "timestamp": str(datetime.utcnow()),
        "endpoint": endpoint,
        "status": status,
        "message": message,
        "data": data
    }
    print(json.dumps(log_entry))  # JSON-style logging
