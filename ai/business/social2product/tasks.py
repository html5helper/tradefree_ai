from ai.core.celery_app import app
from celery import chain, chord
from ai.core.event import Event
from ai.business.social2product.service import DifySocial2ProductService
import json

@app.task
def step_fetch_social_record_total_count(event_in: dict) -> dict:
    """
    获取总记录数并设定分页大小
    """
   
    # 假设获取总记录数的逻辑
    service = DifySocial2ProductService()
    payload = {
        "trace_id": event_in["trace_id"],
        "platform": event_in["context"]["platform"]
    }
    total = service.social_record_total_count(payload)
    print("total:"+str(total))

    page_size = 30
    pages = (total + page_size - 1) // page_size  # 计算总页数
    
    # 更新上下文
    event_out = event_in.copy()
    event_out["context"]["total"] = total
    event_out["context"]["page_size"] = page_size
    event_out["context"]["pages"] = pages

    print("worker.event_out------------>:"+json.dumps(event_out))
        
    return event_out

@app.task
def step_create_products_from_social_page_records(event_in: dict, page: int) -> dict:
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