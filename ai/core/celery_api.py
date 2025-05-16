from fastapi import FastAPI, Request
from celery import chain
from ai.core.celery_app import app as celery_app
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.config.celeryconfig import CHAIN_MAP
from ai.core.data_event import DataEvent
import uuid

api = FastAPI()

def create_workflow_chain(chain_type: str, data: dict):
    """Helper function to create workflow chain"""
    trace_id = str(uuid.uuid4())
    data['trace_id'] = trace_id
    
    event = {
        "data": data,
        "trace_id": trace_id,
        "workflow_name": chain_type
    }

    signatures = []
    for task_name in CHAIN_MAP[chain_type]:
        signatures.append(celery_app.signature(task_name))
    workflow = chain(*signatures)
    # 只给第一个任务传 event，转换为字典以确保可序列化
    result = workflow.apply_async(args=(event,))
    return {"task_id": result.id, "data": event['data']}

@api.post("/workflow/run/amz_to_ali")
async def amz_to_ali(request: Request):
    """Amazon to AliExpress workflow"""
    data = await request.json()
    return create_workflow_chain("amz_to_ali", data)

@api.post("/workflow/run/amz_to_1688")
async def amz_to_1688(request: Request):
    """Amazon to 1688 workflow"""
    data = await request.json()
    return create_workflow_chain("amz_to_1688", data)

@api.post("/workflow/run/1688_to_1688")
async def _1688_to_1688(request: Request):
    """1688 to 1688 workflow"""
    data = await request.json()
    return create_workflow_chain("1688_to_1688", data)

@api.post("/workflow/run/ali_to_ali")
async def ali_to_ali(request: Request):
    """AliExpress to AliExpress workflow"""
    data = await request.json()
    return create_workflow_chain("ali_to_ali", data)

@api.post("/workflow/tasks/retry/{task_id}")
async def retry_task(task_id: str):
    """Retry a failed task and its downstream tasks"""
    return {"task_id": retry_chain_by_task_id(task_id)}

@api.post("/workflow/run/social_to_ali")
async def run_social_to_ali_workflow(request: Request):
    data = await request.json()   
    res = celery_app.send_task('ai.business.social2product.tasks.fetch_social_total', args=[data])
    return {"trace_id": res.id}