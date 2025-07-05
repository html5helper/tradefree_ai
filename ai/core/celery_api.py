from fastapi import FastAPI, Request, Depends
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.core.celery_workflow import CeleryWorkflow
from ai.core.auth.authentication import verify_employee_access_token,verify_sys_token
from ai.core.product_api import api as product_router

api = FastAPI()
workflow = CeleryWorkflow()

# 挂载product_api的路由
api.include_router(product_router)


@api.post("/workflow/run/copy")
async def copy(request: Request, employee_access: dict = Depends(verify_employee_access_token)):
    """Copy and public product workflow"""
    data = await request.json()
    data['access'] = employee_access # 将员工权限信息添加到数据中，用于后续的公共信息提取

    return workflow.create_workflow(data)
    
@api.post("/workflow/run/publish")
async def publish_tob_product(request: Request, employee_access: dict = Depends(verify_employee_access_token)):
    """Publish product workflow"""
    data = await request.json()
    data['access'] = employee_access # 将员工权限信息添加到数据中，用于后续的公共信息提取

    data['use_ai'] = 'false'
    return workflow.create_workflow(data)

@api.post("/workflow/run/social_to_ali")
async def social_to_ali(request: Request, employee_access: dict = Depends(verify_employee_access_token)):
    """Social to AliExpress workflow"""
    data = await request.json()
    data['access'] = employee_access # 将员工权限信息添加到数据中，用于后续的公共信息提取

    data['workflow'] = "social_total"
    return workflow.create_workflow(data)

@api.post("/workflow/tasks/retry/{task_id}")
async def retry_task(task_id: str,sys_access: dict = Depends(verify_sys_token)):
    """Retry a failed task and its downstream tasks"""
    return {"task_id": retry_chain_by_task_id(task_id)}
