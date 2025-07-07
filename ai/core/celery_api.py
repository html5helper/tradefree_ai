from fastapi import FastAPI, Request, Depends, HTTPException
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.core.celery_workflow import CeleryWorkflow
from ai.core.auth.authentication import verify_employee_access_token,verify_sys_token
from ai.core.product_api import api as product_router
from ai.service.product_history_service import ProductHistoryService

product_history_service = ProductHistoryService()

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
    
#发布产品
@api.post("/workflow/run/publish")
async def publish_tob_product(request: Request, employee_access: dict = Depends(verify_employee_access_token)):
    """Publish product workflow"""
    data = await request.json()
    trace_id = data.get("trace_id",None)
    if trace_id == None:
        raise HTTPException(
            status_code=401,
            detail="Need parameter trace_id",
            headers={"WWW-Authenticate": "Bearer"},
        )
    product_history = product_history_service.get_by_trace_id(trace_id=trace_id)
    if product_history == None or product_history.get("publish_product",None) == None:
       raise HTTPException(
            status_code=401,
            detail="Can not find product history with trace_id="+trace_id,
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    parameters = product_history.get("publish_product",None)
    parameters['access'] = employee_access 

    return workflow.create_publish_workflow(parameters)

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
