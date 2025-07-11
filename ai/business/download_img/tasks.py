from ai.core.celery_app import app
from ai.service.dify_service import DifyService
from ai.core.celery_workflow import CeleryWorkflow

service = DifyService()
workflow = CeleryWorkflow()


@app.task
def normal_download_image(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("download_image",data)
