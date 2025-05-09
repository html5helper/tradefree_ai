# ai/core/workflow_state.py
import redis
import json
import threading
from typing import Dict, Any, Optional

class WorkflowState:
    """
    基于 Redis 的状态存储
    """
    _client = redis.Redis(host='localhost', port=6379, db=0)
    _lock = threading.Lock()

    @classmethod
    def create_workflow(cls, trace_id: str, workflow: str, root_event: Dict[str, Any]):
        """
        初始化一个新的 workflow，存入 Redis。
        """
        key = f"wf:{trace_id}"
        data = {
            "event_type": workflow,
            "status": "running",
            "tasks": {},    # event_id -> {name, status, event}
            "pending": {}   # task_name -> [event,...]
        }
        cls._client.set(key, json.dumps(data))
        cls.register_event(trace_id, root_event)

    @classmethod
    def _get(cls, trace_id: str) -> Optional[Dict[str, Any]]:
        val = cls._client.get(f"wf:{trace_id}")
        return json.loads(val) if val else None

    @classmethod
    def _set(cls, trace_id: str, data: Dict[str, Any]):
        cls._client.set(f"wf:{trace_id}", json.dumps(data))

    @classmethod
    def register_event(cls, trace_id: str, event: Dict[str, Any]):
        """
        注册一个新的 task 实例，初始状态为 pending。
        """
        with cls._lock:
            data = cls._get(trace_id)
            data["tasks"][event["event_id"]] = {
                "name": event["event_type"],
                "status": "pending",
                "event": event
            }
            cls._set(trace_id, data)

    @classmethod
    def count_running(cls, trace_id: str, task_name: str) -> int:
        data = cls._get(trace_id)
        return sum(
            1 for t in data["tasks"].values()
            if t["name"] == task_name and t["status"] == "running"
        )

    @classmethod
    def enqueue_pending(cls, trace_id: str, task_name: str, event: Dict[str, Any]):
        """
        并发度已满时，将事件入队 pending。
        """
        with cls._lock:
            data = cls._get(trace_id)
            pend = data["pending"].setdefault(task_name, [])
            pend.append(event)
            cls._set(trace_id, data)

    @classmethod
    def dequeue_pending(cls, trace_id: str, task_name: str) -> Optional[Dict[str, Any]]:
        """
        并发度释放时，从 pending 唤醒一个事件。
        """
        with cls._lock:
            data = cls._get(trace_id)
            pend = data["pending"].get(task_name, [])
            if pend:
                ev = pend.pop(0)
                data["pending"][task_name] = pend
                cls._set(trace_id, data)
                return ev
            return None

    @classmethod
    def mark_running(cls, trace_id: str, event_id: str):
        with cls._lock:
            data = cls._get(trace_id)
            data["tasks"][event_id]["status"] = "running"
            cls._set(trace_id, data)

    @classmethod
    def mark_finished(cls, trace_id: str, event_id: str):
        with cls._lock:
            data = cls._get(trace_id)
            data["tasks"][event_id]["status"] = "finished"
            # 如果所有 tasks 都 finished，则 workflow 结束
            if all(t["status"] == "finished" for t in data["tasks"].values()):
                data["status"] = "finished"
            cls._set(trace_id, data)

    @classmethod
    def get_workflow(cls, trace_id: str) -> Optional[Dict[str, Any]]:
        return cls._get(trace_id)

    @classmethod
    def get_tasks(cls, trace_id: str) -> Dict[str, Any]:
        data = cls._get(trace_id) or {}
        return {
            eid: {"name": info["name"], "status": info["status"]}
            for eid, info in data.get("tasks", {}).items()
        }