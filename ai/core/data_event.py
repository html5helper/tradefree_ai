import uuid
import datetime
from typing import Any, Dict, Optional

class DataEvent:
    def __init__(self, 
                 data: Dict[str, Any],
                 task_name: Optional[str] = None,
                 trace_id: Optional[str] = None,
                 task_id: Optional[str] = None,
                 workflow_name: Optional[str] = None,
                 event_id: Optional[str] = None,
                 timestamp: Optional[str] = None):
        self.trace_id = trace_id
        self.task_id = task_id
        self.task_name = task_name
        self.event_id = event_id or str(uuid.uuid4())
        self.data = data
        self.timestamp = timestamp or (datetime.datetime.utcnow().isoformat() + "Z")
        self.workflow_name = workflow_name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataEvent':
        return cls(
            task_name=data.get('task_name', ''),
            data=data.get('data', {}),
            trace_id=data.get('trace_id'),
            task_id=data.get('task_id'),
            workflow_name=data.get('workflow_name'),
            event_id=data.get('event_id'),
            timestamp=data.get('timestamp')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "task_id": self.task_id,
            "task_name": self.task_name,
            "event_id": self.event_id,
            "data": self.data,
            "timestamp": self.timestamp,
            "workflow_name": self.workflow_name
        }

    def __json__(self):
        """Support for JSON serialization"""
        return self.to_dict()

    def __getstate__(self):
        """Support for pickle serialization"""
        return self.to_dict()

    def __setstate__(self, state):
        """Support for pickle deserialization"""
        self.__dict__.update(state)
