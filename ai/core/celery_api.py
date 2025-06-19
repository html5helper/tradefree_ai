from fastapi import FastAPI, Request, Depends
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.core.celery_workflow import CeleryWorkflow
from ai.core.auth.authentication import verify_token
from ai.core.product_api import api as product_router

api = FastAPI()
workflow = CeleryWorkflow()

# 挂载product_api的路由
api.include_router(product_router)

def parse_data(data: dict, access: dict):
    data['employee_info'] = access.get("employee_info", {})
    workflow = data.get("workflow", None)
    accesses = access.get("employee_accesses", [])
    for item in accesses:
        if item.get("workflow") == workflow:
            data['shop_cn_name'] = item.get("shop_name", None)
            data['action_flow_id'] = item.get("action_flow_id", None)
            break
    return data

@api.post("/workflow/run/copy")
async def copy(request: Request, access: dict = Depends(verify_token)):
    """Copy and public product workflow"""
    data = await request.json()
    data = parse_data(data, access)
    return workflow.create_workflow(data)
    
@api.post("/workflow/run/copy_no_ai")
async def copy_no_ai(request: Request, access: dict = Depends(verify_token)):
    """Copy and public product workflow no ai"""
    data = await request.json()
    data = parse_data(data, access)
    data['use_ai'] = 'false'
    return workflow.create_workflow(data)

@api.post("/workflow/run/social_to_ali")
async def social_to_ali(request: Request, access: dict = Depends(verify_token)):
    """Social to AliExpress workflow"""
    data = await request.json()
    data = parse_data(data, access)
    data['workflow'] = "social_total"
    return workflow.create_workflow(data)

@api.post("/workflow/tasks/retry/{task_id}")
async def retry_task(task_id: str):
    """Retry a failed task and its downstream tasks"""
    return {"task_id": retry_chain_by_task_id(task_id)}
