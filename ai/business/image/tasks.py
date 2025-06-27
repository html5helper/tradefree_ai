from ai.core.celery_app import app
from ai.service.dify_service import DifyService
from ai.core.celery_workflow import CeleryWorkflow

service = DifyService()
workflow = CeleryWorkflow()


@app.task
def image_text_image(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("img2text2img2download",data)

@app.task
def text_image(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("text2img2download",data)

@app.task
def test_image(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.apply(data)


@app.task
def ali_to_ali_image(data: dict):
    data = workflow.build_payload_taskid(data)
    if data.get("product_type") == "silicone":
        return service.run_task("text2img2download",data)
    else:
        return service.run_task("img2text2img2download",data)

@app.task
def social_to_ali_image(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("text2img2download",data)