from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ai.config.celeryconfig import USER_TOKEN_CONFIG
from ai.service.employee_catch_service import EmployeeCacheService

# 创建安全依赖
security = HTTPBearer()
cache_service = EmployeeCacheService()

async def get_user_workflow(request: Request):
    try:
        data = await request.json()

        if data.get("workflow"):
            return data.get("workflow")

        src_platform = data.get("reference_product_platform")
        dest_platform = data.get("published_shop")
        workflow = ""

        # 检查是否是 no_ai 请求
        is_no_ai = "no_ai" in str(request.url)
        key = "copy" if is_no_ai else "to"

        if src_platform == "amazon" and "ali" in dest_platform:
            workflow = f"amz_{key}_ali"
        elif src_platform == "amazon" and "1688" in dest_platform:
            workflow = f"amz_{key}_1688"
        elif src_platform == "ali" and "ali" in dest_platform:
            workflow = f"ali_{key}_ali"
        elif src_platform == "ali" and "1688" in dest_platform:
            workflow = f"ali_{key}_1688"
        elif src_platform == "1688" and "1688" in dest_platform:
            workflow = f"1688_{key}_1688"
        else:
            workflow = ""
    except:
        workflow = ""

    return workflow

async def verify_sys_token(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    """验证系统token"""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.credentials not in USER_TOKEN_CONFIG:
        raise HTTPException(
            status_code=401,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    sys_token = USER_TOKEN_CONFIG[credentials.credentials]

    return sys_token

async def verify_token(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    """验证 Bearer token
    
    Args:
        request: FastAPI 请求对象
        credentials: HTTP 认证凭证
        
    Returns:
        dict: 包含用户信息的字典
        
    Raises:
        HTTPException: 当 token 无效或缺失时抛出
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查是否是 Bearer token
    if not credentials.scheme.lower() == "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 从缓存中获取员工信息
    employee_info = cache_service.get_employee_by_token(credentials.credentials)
    if not employee_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取workflow列表
    workflows = employee_info["workflows"]

    # 获取请求数据和工作流
    try:
        workflow = await get_user_workflow(request)
    except:
        workflow = None

    # 验证用户的workflow权限
    if workflow and workflow not in workflows:
        raise HTTPException(
            status_code=403,
            detail="User does not have access to this workflow",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 添加当前生效的工作流到员工信息中
    employee_info['effective_workflow'] = workflow

    return employee_info
