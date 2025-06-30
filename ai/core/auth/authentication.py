from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ai.config.celeryconfig import USER_TOKEN_CONFIG, USER_GROUP_ACCESS


# 创建安全依赖
security = HTTPBearer()

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
    
    # 验证 token 并获取用户权限信息
    if credentials.credentials not in USER_TOKEN_CONFIG:
        raise HTTPException(
            status_code=401,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户信息
    user_token = credentials.credentials
    user_name = USER_TOKEN_CONFIG[user_token]["user_name"]
    user_group = USER_TOKEN_CONFIG[user_token]["user_group"]
    user_group_access = USER_GROUP_ACCESS[user_group]

    # 获取请求数据和工作流
    try:
        workflow = await get_user_workflow(request)
    except:
        workflow = ""

    # 验证用户的workflow权限
    if workflow and workflow not in user_group_access:
        raise HTTPException(
            status_code=403,
            detail="User does not have access to this workflow",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 构建用户信息字典
    user_info = {
        "user_name": user_name,
        "user_token": user_token,
        "user_group": user_group,
        "user_access": user_group_access,
        "workflow": workflow
    }    
    return user_info
