from api.routes.workflow_api import router as workflow_router
from fastapi import FastAPI
from utils.logging.logger import api_logger
from core.workflow_engine import workflow
import uvicorn

app = FastAPI(title="Tradefree AI Demo")

# 注册路由
app.include_router(workflow_router, prefix="/api/v1")

api_logger.info("API 服务启动完成")

if __name__ == "__main__":
    api_logger.info("开始启动服务...")
    uvicorn.run(app, host="0.0.0.0", port=8000)