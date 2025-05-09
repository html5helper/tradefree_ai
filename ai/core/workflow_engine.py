# ai/core/workflow_engine.py
import os
import yaml
from glob import glob
import uuid
import datetime
from ai.core.workflow_state import WorkflowState
from typing import Dict, Any, Optional

class WorkflowEngine:
    _dags = None

    @classmethod
    def _load_dags(cls) -> Dict[str, Any]:
        if cls._dags is None:
            cls._dags = {}
            dir_path = os.path.join(os.path.dirname(__file__), "..", "workflow")
            for path in glob(os.path.join(dir_path, "*.yaml")):
                with open(path, "r") as f:
                    cfg = yaml.safe_load(f)
                    cls._dags.update(cfg)
        print(cls._dags)
        return cls._dags

    @staticmethod
    def now_iso() -> str:
        return datetime.datetime.utcnow().isoformat() + "Z"

    @classmethod
    def dispatch(cls, event: Dict[str, Any]):
        """
        收到新的 event，注册并根据并行度 either 执行 or 排队。
        """
        from ai.core.event_broker import EventBroker

        dags = cls._load_dags()
        # 确定使用哪个 workflow
        wf_name = event["context"].get("workflow", event["event_type"])
        # 第一次 dispatch 时，把 workflow 写入 context
        event["context"]["workflow"] = wf_name

        conf = dags.get(wf_name)
        if not conf:
            return  # 未配置此 workflow

        tasks_conf = conf["tasks"]
        task_name = event["event_type"]
        task_conf = tasks_conf.get(task_name)
        if not task_conf:
            return  # 未配置此 task

        trace_id = event["trace_id"]
        # 注册 task 实例
        WorkflowState.register_event(trace_id, event)

        # 并行度判断
        concurrency = task_conf.get("concurrency", 1)
        running = WorkflowState.count_running(trace_id, task_name)
        if running < concurrency:
            WorkflowState.mark_running(trace_id, event["event_id"])
            EventBroker.send_to_worker(event)
        else:
            WorkflowState.enqueue_pending(trace_id, task_name, event)

    @classmethod
    def handle_task_complete(cls, event: Dict[str, Any]):
        """
        Task 执行成功后回调：标记 finished，唤醒 pending，并触发下游 tasks。
        """
        dags = cls._load_dags()
        wf_name = event["context"]["workflow"]
        conf = dags.get(wf_name, {})
        tasks_conf = conf.get("tasks", {})

        trace_id = event["trace_id"]
        task_name = event["event_type"]
        event_id  = event["event_id"]

        # 标记完成
        WorkflowState.mark_finished(trace_id, event_id)

        # 唤醒一个同名 pending
        pending = WorkflowState.dequeue_pending(trace_id, task_name)
        if pending:
            cls.dispatch(pending)

        # 下游 tasks
        for nxt in tasks_conf.get(task_name, {}).get("next", []):
            new_event = {
                "event_id": str(uuid.uuid4()),
                "trace_id": trace_id,
                "event_type": nxt,
                "payload": {},  # 需要时可从 event["payload"] 中提取
                "context": event["context"].copy(),
                "timestamp": cls.now_iso()
            }
            cls.dispatch(new_event)