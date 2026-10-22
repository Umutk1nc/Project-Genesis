import json
import os
from pathlib import Path

project = Path(__file__).parent.parent.parent
EVENT_PATH = project / "data" / "processed" / "events.json"

with open(EVENT_PATH, "r", encoding="utf-8") as file:
    events = json.load(file)

print(events)