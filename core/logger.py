import json
import datetime

class AuditLogger:
    def __init__(self, log_file="hades_audit.jsonl"):
        self.log_file = log_file

    def log(self, event_type, data):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "data": data
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + "\n")

    def replay(self):
        with open(self.log_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                print(f"[{entry['timestamp']}] {entry['event_type']}: {entry['data']}")
