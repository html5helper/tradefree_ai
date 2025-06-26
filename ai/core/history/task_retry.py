from ai.core.celery_app import app as celery_app
from celery import chain
from fastapi import HTTPException
from ai.config.celeryconfig import CHAIN_MAP
from ai.service.task_event_service import TaskEventService

task_event_service = TaskEventService()

def retry_chain_by_task_id(task_id: str):
    task_event = task_event_service.get(task_id)
    if not task_event:
        raise HTTPException(status_code=404, detail="Task history not found")
    
    # retried字段置为1
    task_event.retried = 1
    task_event_service.update(task_id, {'retried': 1})

    task_name = task_event.task_name
    args = task_event.task_input or []
    event = args[0] if args else None
    if not event:
        raise HTTPException(status_code=400, detail="No event found in args")

    # 判断属于哪个chain
    chain_type = None
    for key in CHAIN_MAP:
        if key in task_name:
            chain_type = key
            break
    if not chain_type:
        raise HTTPException(status_code=400, detail="Unsupported chain for this task")

    task_list = CHAIN_MAP[chain_type]
    # 找到失败任务在chain中的位置
    try:
        idx = task_list.index(task_name)
    except ValueError:
        raise HTTPException(status_code=400, detail="Task name not found in chain definition")

    # 取失败任务及其之后的任务（包含失败任务本身）
    next_tasks = task_list[idx:]
    if not next_tasks:
        raise HTTPException(status_code=400, detail="No downstream tasks to retry")

    # 构建新的chain
    signatures = []
    if next_tasks:
        signatures.append(celery_app.signature(next_tasks[0], args=(event,)))
        for t in next_tasks[1:]:
            signatures.append(celery_app.signature(t))
    workflow = chain(*signatures)
    data = {"trace_id": task_event.trace_id,"task_id": task_event.task_id}
    result = workflow.apply_async(args=(data,))
    
    return result.id