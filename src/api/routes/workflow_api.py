from fastapi import APIRouter, HTTPException
from core.event import Event, event_manager
from datetime import datetime
from utils.logging.logger import api_logger

router = APIRouter()

@router.post("/trigger-workflow")
async def trigger_workflow(data: dict):
    """触发工作流"""
    try:
        api_logger.info(f"收到工作流触发请求: {data}")
        # 创建并触发 event_001
        event = Event(
            event_id=f"event_001_{datetime.now().timestamp()}",
            event_type="event_001",
            data=data
        )
        event_manager.trigger_event(event)
        
        api_logger.info(f"工作流触发成功: {event.event_id}")
        return {
            "status": "success",
            "message": "Workflow triggered successfully",
            "event_id": event.event_id
        }
    except Exception as e:
        api_logger.error(f"工作流触发失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))