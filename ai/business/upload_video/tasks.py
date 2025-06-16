from ai.core.celery_app import app
from ai.business.service.dify_service import DifyService
from ai.core.celery_workflow import CeleryWorkflow

service = DifyService()
workflow = CeleryWorkflow()


@app.task
def amz_to_ali_upload(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("upload_video",data)

@app.task
def amz_to_1688_upload(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("upload_video",data)

@app.task
def ali_to_1688_upload(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("upload_video",data)

@app.task
def _1688_to_1688_upload(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("upload_video",data)

@app.task
def ali_to_ali_upload(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("upload_video",data)
