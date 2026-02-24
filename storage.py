import json
import os
from typing import Set

def load_sent_notifications(path: str = "sent_matches.json") -> Set[str]:
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_sent_notification(sent_set: Set[str], match_id: str, path: str = "sent_matches.json") -> None:
    sent_set.add(match_id)
    with open(path, "w") as f:
        json.dump(sorted(sent_set), f, indent=2)