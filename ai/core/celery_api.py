from fastapi import FastAPI, Request
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.core.celery_workflow import CeleryWorkflow

api = FastAPI()
workflow = CeleryWorkflow()

@api.post("/workflow/run/amz_to_ali")
async def amz_to_ali(request: Request):
    """Amazon to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("amz_to_ali", data)

@api.post("/workflow/run/amz_to_1688")
async def amz_to_1688(request: Request):
    """Amazon to 1688 workflow"""
    data = await request.json()
    return workflow.create_workflow("amz_to_1688", data)

@api.post("/workflow/run/1688_to_1688")
async def _1688_to_1688(request: Request):
    """1688 to 1688 workflow"""
    data = await request.json()
    return workflow.create_workflow("1688_to_1688", data)

@api.post("/workflow/run/ali_to_ali")
async def ali_to_ali(request: Request):
    """AliExpress to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("ali_to_ali", data)

@api.post("/workflow/run/social_to_ali")
async def social_to_ali(request: Request):
    """Social to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("social_total", data)

@api.post("/workflow/tasks/retry/{task_id}")
async def retry_task(task_id: str):
    """Retry a failed task and its downstream tasks"""
    return {"task_id": retry_chain_by_task_id(task_id)}

