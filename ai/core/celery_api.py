from fastapi import FastAPI, Request, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.core.celery_workflow import CeleryWorkflow
from ai.config.celeryconfig import API_KEY
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建安全依赖
security = HTTPBearer()

# 验证 token 的函数
async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
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
    
    # 验证 token
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials

api = FastAPI()
workflow = CeleryWorkflow()

@api.post("/workflow/run/copy")
async def amz_to_ali(request: Request, token: str = Depends(verify_token)):
    """Copy and public product workflow"""
    data = await request.json()
    reference_product_platform = data.get("reference_product_platform")
    published_shop = data.get("published_shop")

    if reference_product_platform == "amazon" and "ali" in published_shop:
        return workflow.create_workflow("amz_to_ali", data)
    elif reference_product_platform == "amazon" and "1688" in published_shop:
        return workflow.create_workflow("amz_to_1688", data)
    elif reference_product_platform == "ali" and "ali" in published_shop:
        return workflow.create_workflow("ali_to_ali", data)
    elif reference_product_platform == "ali" and "1688" in published_shop:
        return workflow.create_workflow("ali_to_1688", data)
    elif reference_product_platform == "1688" and "1688" in published_shop:
        return workflow.create_workflow("1688_to_1688", data)
    else:
        return {"error": "Invalid reference_product_platform or published_shop"}

@api.post("/workflow/run/amz_to_ali")
async def amz_to_ali(request: Request, token: str = Depends(verify_token)):
    """Amazon to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("amz_to_ali", data)

@api.post("/workflow/run/amz_to_1688")
async def amz_to_1688(request: Request, token: str = Depends(verify_token)):
    """Amazon to 1688 workflow"""
    data = await request.json()
    return workflow.create_workflow("amz_to_1688", data)

@api.post("/workflow/run/ali_to_1688")
async def ali_to_1688(request: Request, token: str = Depends(verify_token)):
    """AliExpress to 1688 workflow"""
    data = await request.json()
    return workflow.create_workflow("ali_to_1688", data)

@api.post("/workflow/run/1688_to_1688")
async def _1688_to_1688(request: Request, token: str = Depends(verify_token)):
    """1688 to 1688 workflow"""
    data = await request.json()
    return workflow.create_workflow("1688_to_1688", data)

@api.post("/workflow/run/ali_to_ali")
async def ali_to_ali(request: Request, token: str = Depends(verify_token)):
    """AliExpress to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("ali_to_ali", data)

@api.post("/workflow/run/social_to_ali")
async def social_to_ali(request: Request, token: str = Depends(verify_token)):
    """Social to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("social_total", data)

@api.post("/workflow/tasks/retry/{task_id}")
async def retry_task(task_id: str, token: str = Depends(verify_token)):
    """Retry a failed task and its downstream tasks"""
    return {"task_id": retry_chain_by_task_id(task_id)}

