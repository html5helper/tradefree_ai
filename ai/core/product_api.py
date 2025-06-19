from fastapi import APIRouter, Request, Depends
from ai.core.auth.authentication import verify_token, verify_sys_token
from ai.service.employee_service import EmployeeService
from ai.service.employee_catch_service import EmployeeCacheService
from ai.dao.db.engine import manager_engine, workflow_engine
from sqlalchemy.orm import Session
from ai.dao.entity.action_flow import ActionFlow


api = APIRouter()

# -------------------------------------------
# Service
# -------------------------------------------
manager_session = Session(bind=manager_engine)
workflow_session = Session(bind=workflow_engine)
employee_service = EmployeeService()
cache_service = EmployeeCacheService()

# -------------------------------------------
# System API
# -------------------------------------------

@api.post("/client/employee/refresh")
async def employee_refresh(request: Request, sys_token: dict = Depends(verify_sys_token)):
    """Refresh Employee catch"""
    data = await request.json()
    employee_id = data.get('employee_id')
    
    result = employee_service.refresh_employee_access_catch(employee_id)
    return {"code": 200, "message": "success","data":{"result":result}}

@api.post("/client/employee/refresh_all")
async def employee_refresh_all(request: Request, sys_token: dict = Depends(verify_sys_token)):
    """Refresh all Employees catch"""
    
    counts = employee_service.refresh_employee_accesses_catch()
    return {"code": 200, "message": "success","data":{"counts":counts}}

# -------------------------------------------
# Client API
# -------------------------------------------
@api.post("/client/employee/activate")
async def employee_activate(request: Request, employee_info: dict = Depends(verify_token)):
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

@api.post("/client/actionflow/get")
async def product_list(request: Request, user_info: dict = Depends(verify_token)):
    """Get Actionflow By Actionflow ID"""
    data = await request.json()
    actionflow_id = data['actionflow_id']
    # 查询Actionflow信息
    actionflow = manager_session.query(ActionFlow).filter(
        ActionFlow.id == actionflow_id,
        ActionFlow.is_enable == True
    ).first()
            
    if not actionflow:
        return {"code": 404, "message": "Actionflow not found", "data": None}

    return {"code": 200, "message": "success","data":actionflow.to_dict()}

@api.post("/client/product/platform")
async def product_list(request: Request, user_info: dict = Depends(verify_token)):
    """Get Product List By platform"""
    data = await request.json()
    platform = data['platform']
    platform_product_list = []
    return {"code": 200, "message": "success","data":platform_product_list}

@api.post("/client/product/all")
async def product_list(request: Request, access_info: dict = Depends(verify_token)):
    """Get All Platform Product List"""
    data = await request.json()
    employee_info = access_info['employee_info']
    employee_name = employee_info['employee_name']

    platform = data.get('platform')
    product_type = data.get('product_type')
    product_list = []
    if platform:
        product_list = workflow_session.query(Product).filter(Product.platform == platform).all()
    elif product_type:
        product_list = workflow_session.query(Product).filter(Product.product_type == product_type).all()
    else:
        product_list = session.query(Product).all()
    return {"code": 200, "message": "success","data":product_list}

# -------------------------------------------
