from dataclasses import dataclass
from typing import Any, Dict, Optional
import uuid
import datetime

@dataclass
class Event:
    """
    Generic event structure for workflow processing
    """

    @staticmethod
    def get_event_template(event_type:str):
        """Convert event to dictionary"""
        obj = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "trace_id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "payload": {},
            "context": {},
            "metadata": {}
        }
        return obj
