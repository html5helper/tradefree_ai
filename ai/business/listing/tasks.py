from ai.core.celery_app import app
from ai.service.dify_service import DifyService
from ai.core.celery_workflow import CeleryWorkflow

service = DifyService()
workflow = CeleryWorkflow()

@app.task
def amz_to_ali_listing(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("product_listing",data)

@app.task
def amz_to_1688_listing(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("product_listing",data)

@app.task
def ali_to_1688_listing(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("product_listing",data)

@app.task
def _1688_to_1688_listing(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("product_listing",data)

@app.task
def ali_to_ali_listing(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("product_listing",data)

@app.task
def listing_adapter(data: dict):
    data = workflow.build_payload_taskid(data)
    return service.run_task("listing_adapter",data)

@app.task
def social_to_ali_listing(data: dict):
    data = workflow.build_payload_taskid(data)
    # 获取指定页的记录中适合生成listing的记录
    result = service.run_task("social_pages_listing", data)
    items = result['items']
    # 循环处理每个listing
    for item in items:
        workflow.create_workflow("social_to_ali", item)

    return len(items)