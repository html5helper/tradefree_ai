from fastapi import APIRouter, Request, Depends
from ai.core.auth.authentication import verify_sys_token,verify_employee_token
from ai.service.employee_service import EmployeeService
from ai.service.employee_catch_service import EmployeeCacheService
from ai.service.product_publish_service import ProductPublishService
from ai.dao.db.engine import manager_engine, workflow_engine
from sqlalchemy.orm import Session
from ai.dao.entity.action_flow import ActionFlow
from ai.service.actionflow_service import ActionFlowService
import json

api = APIRouter()

# -------------------------------------------
# Service
# -------------------------------------------
manager_session = Session(bind=manager_engine)
workflow_session = Session(bind=workflow_engine)
employee_service = EmployeeService()
cache_service = EmployeeCacheService()
product_publish_service = ProductPublishService()
actionflow_service = ActionFlowService()

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


@api.post("/workflow/product/platform")
async def product_list(request: Request, access: dict = Depends(verify_employee_token)):
    """Get Product List By platform"""
    data = await request.json()
    platform = data.get('platform',None)
    product_type = data.get('product_type',None)
    employee_info = access['employee_info']
    employee_id = employee_info['employee_id']
    # model: publish, collect, history
    model = data.get('model',"publish")
    if model == "publish":
        status_list = ['READY']
    elif model == "collect":
        status_list = ['GENERATING','READY']
    elif model == "history":
        status_list = ['SUCCESS','FAILED']
    
    # 使用关键字参数，避免位置参数问题
    product_publish_list = product_publish_service.list_by_employee_and_platform_and_product_type(
        employee_id=employee_id, 
        platform=platform, 
        product_type=product_type, 
        status_list=status_list
    )

    products = []
    workflow_ids = []
    for product_publish in product_publish_list:
        if product_publish.product and product_publish.product != "":
            prod_item = json.loads(product_publish.product)
            product_publish.product = prod_item
            products.append(prod_item)
        if(not product_publish.action_flow_id in workflow_ids):
            workflow_ids.append(product_publish.action_flow_id)

    actionflow_list = actionflow_service.get_by_ids(workflow_ids)
    actionflows = {}
    for actionflow in actionflow_list:
        actionflows[actionflow.id] = actionflow.action_flow

    result = {
        "code": 200,
        "message": "success",
        "data": {
            "product_list": product_publish_list,
            "products": products,
            "actionflows": actionflows
        }
    }

    return result
