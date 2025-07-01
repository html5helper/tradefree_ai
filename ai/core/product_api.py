from fastapi import APIRouter, Request, Depends
from ai.core.auth.authentication import verify_sys_token,verify_employee_token
from ai.service.employee_service import EmployeeService
from ai.service.employee_catch_service import EmployeeCacheService
from ai.service.product_history_service import ProductHistoryService
from ai.dao.db.engine import manager_engine, workflow_engine
from sqlalchemy.orm import Session
from ai.dao.entity.action_flow import ActionFlow
from ai.service.actionflow_service import ActionFlowService
from ai.core.history.task_retry import retry_chain_by_task_id
import json
from datetime import datetime
from ai.service.dify_service import DifyService

api = APIRouter()

# -------------------------------------------
# Service
# -------------------------------------------
manager_session = Session(bind=manager_engine)
workflow_session = Session(bind=workflow_engine)
employee_service = EmployeeService()
cache_service = EmployeeCacheService()
product_history_service = ProductHistoryService()
actionflow_service = ActionFlowService()
dify_service = DifyService()

# -------------------------------------------
# System API
# -------------------------------------------

@api.post("/workflow/employee/refresh")
async def employee_refresh(request: Request, sys_token: dict = Depends(verify_sys_token)):
    """Refresh Employee catch"""
    data = await request.json()
    employee_id = data.get('employee_id')
    
    result = employee_service.refresh_employee_access_catch(employee_id)
    return {"code": 200, "message": "success","data":{"result":result}}

@api.post("/workflow/employee/refresh_all")
async def employee_refresh_all(request: Request, sys_token: dict = Depends(verify_sys_token)):
    """Refresh all Employees catch"""
    
    counts = employee_service.refresh_employee_accesses_catch()
    return {"code": 200, "message": "success","data":{"counts":counts}}

# -------------------------------------------
# Client API
# -------------------------------------------
@api.post("/workflow/employee/activate")
async def employee_activate(request: Request, employee_info: dict = Depends(verify_employee_token)):
    """Employer activate
    
    Args:
        request: FastAPI request object
        employee_info: User information from token verification
        
    Returns:
        dict: Response containing employer information in the same format as get_employee_access_by_token
        {
            "code": int,
            "message": str,
            "data": {
                "token": {
                    "user_info": {
                        "user_name": str,
                        "user_group": str,
                    },
                    "employer_info": {
                        "employer_id": str,
                        "employer_name": str,
                        "employer_cn_name": str
                    },
                    "employer_accesses": [
                        {
                            "employer_id": str,
                            "workflow": str,
                            "workflow_name": str,
                            "product_type": str,
                            "platform": str,
                            "category_id": str,
                            "shop_name": str,
                            "action_flow_id": str
                        }
                    ],
                    "workflows": [],
                    "actionflows": []
                }
            }
        }
    """
    try:
        if not employee_info:
            return {"code": 404, "message": "Employee not found or token is invalid", "data": None}
        
        return {"code": 200, "message": "success", "data": employee_info}
        
    except Exception as e:
        print(f"Error in employer_activate: {str(e)}")
        return {"code": 500, "message": f"Internal server error: {str(e)}", "data": None}

@api.post("/workflow/product/list")
async def product_list(request: Request, access: dict = Depends(verify_employee_token)):
    """Get Product List By platform"""
    data = await request.json()
    platform = data.get('platform',None)
    product_type = data.get('product_type',None)
    employee_info = access['employee_info']
    employee_id = employee_info['employee_id']
    start_time_str = data.get('start_time',None)
    end_time_str = data.get('end_time',None)

    # 转换时间字符串为datetime对象
    start_time = None
    end_time = None
    if start_time_str:
        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        except:
            start_time = None
    if end_time_str:
        try:
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        except:
            end_time = None

    # model: collect, generate, publish,published
    model = data.get('model',"published")
    if model == "collect":
        product_publish_list = product_history_service.collect_list(employee_id=employee_id, platform=platform, product_type=product_type)
    elif model == "generate":
        product_publish_list = product_history_service.generate_list(employee_id=employee_id, platform=platform, product_type=product_type)
    elif model == "publish":
        product_publish_list = product_history_service.publish_list(employee_id=employee_id, platform=platform, product_type=product_type)
    elif model == "published":
        if start_time and end_time:
            product_publish_list = product_history_service.published_list(employee_id=employee_id, platform=platform, product_type=product_type,start_time=start_time,end_time=end_time)
        else:
            product_publish_list = []
    else:
        product_publish_list = []

    # products = []
    workflow_ids = []
    for product_publish in product_publish_list:
        if product_publish.get('collect_product') and product_publish['collect_product'] != "":
            prod_item = json.loads(product_publish['collect_product'])
            product_publish['collect_product'] = prod_item
        if product_publish.get('generate_product') and product_publish['generate_product'] != "":
            prod_item = json.loads(product_publish['generate_product'])
            # 如果img_url为数组，则将其转化为逗号分隔的 string
            if (prod_item.get('img_url') and isinstance(prod_item['img_url'], list)):
                prod_item['img_url'] = ','.join(prod_item['img_url'])
            product_publish['generate_product'] = prod_item
        if product_publish.get('publish_product') and product_publish['publish_product'] != "":
            prod_item = json.loads(product_publish['publish_product'])
            product_publish['publish_product'] = prod_item
        if(not product_publish.get('action_flow_id') in workflow_ids):
            workflow_ids.append(product_publish['action_flow_id'])

    actionflow_list = actionflow_service.get_by_ids(workflow_ids)
    actionflows = {}
    for actionflow in actionflow_list:
        actionflows[actionflow['id']] = actionflow['action_flow']

    result = {
        "code": 200,
        "message": "success",
        "data": {
            "product_list": product_publish_list,
            "actionflows": actionflows
        }
    }

    return result

@api.post("/workflow/product/delete")
async def product_delete(request: Request, access: dict = Depends(verify_employee_token)):
    """Delete Product By trace_id"""
    data = await request.json()
    trace_id = data.get('trace_id',None)
    result = product_history_service.delete_by_trace_id(trace_id)
    return {"code": 200, "message": "success","data":{"result":result}}


@api.post("/workflow/product/retry")
async def retry_product_task(request: Request,access: dict = Depends(verify_employee_token)):
    """Retry a failed task and its downstream tasks"""
    data = await request.json()
    task_id = data.get('task_id',None)
    return {"task_id": retry_chain_by_task_id(task_id)}

@api.post("/workflow/image/inpaint")
async def image_inpaint(request: Request,access: dict = Depends(verify_employee_token)):
    """Image Inpaint"""
    data = await request.json()
    result = dify_service.image_inpaint(data)
    return result