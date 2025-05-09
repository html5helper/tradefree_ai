from ai.core.celery_app import app
from celery import chain, chord
from ai.core.event import Event
from ai.business.social2product.service import DifySocial2ProductService
from ai.core.event_broker import EventBroker
from ai.core.workflow_state import WorkflowState
import json

@app.task(bind=True)
def fetch_social_total(event_in: dict):
    """
    获取总记录数并设定分页大小
    """
    WorkflowState.mark_running(event_in["trace_id"], event_in["task_name"])

  # event 为上述 Event JSON
    trace_id = event_in["trace_id"]
    platform = event_in["context"]["platform"] 
    
    # 假设获取总记录数的逻辑
    service = DifySocial2ProductService()
    payload = {
        "trace_id": trace_id,
        "platform": platform
    }
    total = service.social_record_total_count(payload)

    page_size = 30
    pages = (total + page_size - 1) // page_size  # 计算总页数

    event_out = {
      **event_in,
      "task_name": "step_fetch_total",
      "status": "SUCCESS",
      "result": {"total": total, "pages": pages, "page_size": page_size}
    }

    # 更新状态存储
    WorkflowState.mark_finished(trace_id, event_in["task_name"], {"total": total, "pages": pages, "page_size": page_size})

    print("worker.event_out------------>:"+json.dumps(event_out))

    # 上报完成事件给 Engine
    EventBroker.publish(event_out)


@app.task
def create_social_product_by_page(event_in: dict, page: int) -> dict:
    """
    根据页码处理分页记录
    """
    
    # 处理当前页的记录逻辑
    print(f"Processing page {page}")
    service = DifySocial2ProductService()
    payload = {
        "trace_id": event_in["trace_id"],
        "platform": event_in["context"]["platform"],
        "page": page,
        "page_size": event_in["context"]["page_size"]
    } 
    urls = service.create_products_from_social_page_records(payload)
    event_out = event_in.copy()
    event_out["payload"] = {"urls":urls}

    # Convert back to dict for Celery
    return event_out

@app.task
def step_output_results(event: dict) -> dict:
    """
    Step 3: Output and return the urls
    """
    # Convert dict to Event object
    evt = Event.from_dict(event)
    
    # Get result url
    urls = evt.payload["result"]["outputs"]["urls"]

    
    # Return result
    return {
        "event_id": evt.event_id,
        "trace_id": evt.trace_id,
        "count": len(urls),
        "urls": urls
    }

@app.task
def run_workflow(event: dict):
    """
    主工作流，获取总记录数并分页处理
    """
    # 创建任务链
    workflow = chain(
        step_fetch_social_record_total_count.s(event),
        create_page_tasks.s()  # 假设 create_page_tasks 是一个处理分页任务的函数
    )
    
    # 启动工作流
    return workflow.apply_async()

@app.task
def create_page_tasks(event: dict):
    """
    根据总记录数创建分页任务
    """
    pages = event.get("context", {}).get("pages", 1)
    print("pages:" + str(pages))

    # 创建分页任务链
    page_tasks = []
    for page_idx in range(pages):
        page_task = step_create_products_from_social_page_records.s(event, page_idx+1)
        page_tasks.append(page_task)

    # 串行执行分页任务
    return chain(*page_tasks).apply_async()