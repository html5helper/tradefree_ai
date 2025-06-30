from fastapi import FastAPI, Request, Depends
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.core.celery_workflow import CeleryWorkflow
from ai.core.auth.authentication import verify_token
from ai.core.product_api import api as product_router

api = FastAPI()
workflow = CeleryWorkflow()

# 挂载product_api的路由
api.include_router(product_router)

@api.post("/workflow/run/copy")
async def copy(request: Request, access: dict = Depends(verify_token)):
    """Copy and public product workflow"""
    data = await request.json()
    workflow_name = access.get("workflow", "")
    print("workflow_name="+workflow_name+",data="+str(data))
    if not workflow_name:
        return {"error": "Invalid workflow"}
    return workflow.create_workflow(workflow_name, data)
    
@api.post("/workflow/run/copy_no_ai")
async def copy_no_ai(request: Request, access: dict = Depends(verify_token)):
    """Copy and public product workflow no ai"""
    data = await request.json()
    data['use_ai'] = 'false'
    workflow_name = access.get("workflow", "")
    
    if not workflow_name:
        return {"error": "Invalid workflow"}
    return workflow.create_workflow(workflow_name, data)

@api.post("/workflow/run/social_to_ali")
async def social_to_ali(request: Request, user_info: dict = Depends(verify_token)):
    """Social to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("social_total", data)

@api.post("/workflow/tasks/retry/{task_id}")
async def retry_task(task_id: str):
    """Retry a failed task and its downstream tasks"""
    return {"task_id": retry_chain_by_task_id(task_id)}
