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
    def create(event_type:str, task_name:str, trace_id:str):
        """Convert event to dictionary"""
        obj = {
            "event_id": str(uuid.uuid4()),
            "trace_id": trace_id,
            "event_type": event_type,
            "task_name": task_name,
            "payload": {}, # 任务输入
            "result": {}, # 任务输出
            "context": {}, # 上下文
            "status": "PENDING", # 任务状态
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        return obj
