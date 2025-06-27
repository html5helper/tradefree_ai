from ai.core.celery_app import app
from ai.service.dify_service import DifyService
from ai.core.celery_workflow import CeleryWorkflow

service = DifyService()
workflow = CeleryWorkflow()

@app.task
def api_publish_product(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("publish_product",data)

@app.task
def test_publish_product(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.apply(data)