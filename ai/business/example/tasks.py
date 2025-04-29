from celery import chain, shared_task
from ai.celery_app import app
import time
import logging
import uuid

logger = logging.getLogger(__name__)

@shared_task
def task1(params: dict) -> dict:
    """示例任务1"""
    trace_id = params.get('trace_id', 'unknown')
    logger.info(f"[{trace_id}] Starting task1 with params: {params}")
    time.sleep(2)
    result = {"status": "success", "message": "Task 1 completed"}
    logger.info(f"[{trace_id}] Task1 completed with result: {result}")
    return result

@shared_task
def task2(params: dict) -> dict:
    """示例任务2"""
    trace_id = params.get('trace_id', 'unknown')
    logger.info(f"[{trace_id}] Starting task2 with params: {params}")
    time.sleep(3)
    result = {"status": "success", "message": "Task 2 completed"}
    logger.info(f"[{trace_id}] Task2 completed with result: {result}")
    return result

@shared_task
def task3(params: dict) -> dict:
    """示例任务3"""
    trace_id = params.get('trace_id', 'unknown')
    logger.info(f"[{trace_id}] Starting task3 with params: {params}")
    time.sleep(1)
    result = {"status": "success", "message": "Task 3 completed"}
    logger.info(f"[{trace_id}] Task3 completed with result: {result}")
    return result

def start_workflow(a: int, b: int, trace_id: str = None) -> dict:
    """启动工作流
    
    Args:
        a: 第一个参数
        b: 第二个参数
        trace_id: 可选的跟踪ID，如果不提供则自动生成
        
    Returns:
        dict: 包含工作流执行信息的字典
    """
    trace_id = trace_id or str(uuid.uuid4())
    
    # 创建任务链
    workflow = chain(
        task1.s({"a": a, "b": b, "trace_id": trace_id}),
        task2.s(),
        task3.s()
    )
    
    # 执行工作流
    result = workflow.apply_async()
    
    return {
        "trace_id": trace_id,
        "task_id": result.id
    } 