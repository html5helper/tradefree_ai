# ai/core/event_broker.py
from celery import Celery
from celery.signals import task_success
from typing import Dict, Any
import os

app = Celery('tradefree_ai')
app.config_from_object('ai.config.celeryconfig')

class EventBroker:
    @staticmethod
    def publish(event: Dict[str, Any]):
        from ai.core.workflow_engine import WorkflowEngine
        """
        API 或内部触发第一个 event。
        """
        WorkflowEngine.dispatch(event)

    @staticmethod
    def send_to_worker(event: Dict[str, Any]):
        """
        真正下发给 Celery worker 的调用。
        约定：task 名称 == event_type
        """
        queue = event["context"]["workflow"] + "_tasks"
        app.send_task(
            name=event["event_type"],
            args=[event],
            kwargs={},
            queue=queue
        )

    @staticmethod
    def on_task_success(sender=None, result=None, **kwargs):
        """
        Celery 任务成功回调，读取 result 中返回的 event 字段触发后续。
        """
        ev = result.get("event")
        if ev:
            WorkflowEngine.handle_task_complete(ev)

# 注册回调
task_success.connect(EventBroker.on_task_success)