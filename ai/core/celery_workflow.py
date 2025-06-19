from celery import chain
from ai.core.celery_app import app as celery_app
from ai.config.celeryconfig import CHAIN_MAP
from celery import current_task
import uuid

class CeleryWorkflow:
    def __init__(self):
        self.celery_app = celery_app

    def create_workflow(self, data: dict):
        """Helper function to create workflow chain"""
        trace_id = str(uuid.uuid4())
        data['trace_id'] = trace_id
        chain_type = data.get("workflow", None)
        data['workflow_name'] = chain_type

        signatures = []
        for task_name in CHAIN_MAP[chain_type]:
            signatures.append(celery_app.signature(task_name))
        workflow = chain(*signatures)
        # 只给第一个任务传 event，转换为字典以确保可序列化
        result = workflow.apply_async(args=(data,))
        return {"task_id": result.id, "data": data}
    
    def build_payload_taskid(self,data:dict):
        """
        构建payload，添加task_id
        """
        data['task_id'] = current_task.request.id
        return data
