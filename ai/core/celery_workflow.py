from celery import chain
from ai.core.celery_app import app as celery_app
from ai.config.celeryconfig import CHAIN_MAP,TOB_PUBLISH_WORKFLOW_CHAIN
from celery import current_task
import uuid

class CeleryWorkflow:
    def __init__(self):
        self.celery_app = celery_app

    def create_workflow(self, data: dict):
        """Helper function to create workflow chain"""
        if not data.get("trace_id"):
            data['trace_id'] = str(uuid.uuid4())
        workflow = data.get("workflow", None)

        signatures = []
        for task_name in CHAIN_MAP[workflow]:
            signatures.append(celery_app.signature(task_name))
        workflow = chain(*signatures)
        # 只给第一个任务传 event，转换为字典以确保可序列化
        result = workflow.apply_async(args=(data,))
        return {"task_id": result.id, "trace_id": data['trace_id'],"message": "success"}
    
    def create_publish_workflow(self, data: dict):
        """Helper function to create publish workflow chain"""

        signatures = []
        for task_name in TOB_PUBLISH_WORKFLOW_CHAIN:
            signatures.append(celery_app.signature(task_name))
        workflow = chain(*signatures)
        # 只给第一个任务传 event，转换为字典以确保可序列化
        result = workflow.apply_async(args=(data,))
        return {"task_id": result.id, "trace_id": data['trace_id'],"message": "success"}
    
    def build_payload_taskid(self,data:dict):
        """
        构建payload，添加task_id
        """
        data['task_id'] = current_task.request.id
        return data
