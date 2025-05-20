from ai.core.celery_app import app
from ai.business.service.dify_service import DifyService
from ai.core.celery_workflow import CeleryWorkflow

service = DifyService()
workflow = CeleryWorkflow()

@app.task
def amz_to_ali_src(data: dict):
    return service.apply(data)

@app.task
def amz_to_1688_src(data: dict):
    return service.apply(data)

@app.task
def ali_to_1688_src(data: dict):
    return service.apply(data)

@app.task
def _1688_to_1688_src(data: dict):
    return service.apply(data)

@app.task
def ali_to_ali_src(data: dict):
    return service.apply(data)

@app.task
def social_to_ali_src(data: dict):
    # 获取总条数
    result = service.run_task("social_fetch_total", data)
    total = int(result['total'])
    # 获取page_size
    page_size = int(data['page_size'])
    # 获取总页数
    pages = int(total / page_size)

    # 循环处理每页,page 从1开始
    for page in range(1, pages+1):
        data_copy = data.copy()
        data_copy['page'] = page
        workflow.create_workflow("social_pages", data_copy)

    return total
