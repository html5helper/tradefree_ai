from ai.core.celery_app import app as celery_app
from celery import chain
from ai.core.history.task_event import TaskEvent
from ai.core.db.engine import workflow_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from ai.config.celeryconfig import CHAIN_MAP

Session = sessionmaker(bind=workflow_engine)

def retry_chain_by_task_id(task_id: str):
    session = Session()
    history = session.query(TaskEvent).filter_by(task_id=task_id).first()
    if not history:
        session.close()
        raise HTTPException(status_code=404, detail="Task history not found")
    
    # retried字段置为1
    history.retried = 1
    session.commit()

    task_name = history.task_name
    args = history.task_input or []
    event = args[0] if args else None
    if not event:
        session.close()
        raise HTTPException(status_code=400, detail="No event found in args")

    # 判断属于哪个chain
    chain_type = None
    for key in CHAIN_MAP:
        if key in task_name:
            chain_type = key
            break
    if not chain_type:
        session.close()
        raise HTTPException(status_code=400, detail="Unsupported chain for this task")

    task_list = CHAIN_MAP[chain_type]
    # 找到失败任务在chain中的位置
    try:
        idx = task_list.index(task_name)
    except ValueError:
        session.close()
        raise HTTPException(status_code=400, detail="Task name not found in chain definition")

    # 取失败任务及其之后的任务（包含失败任务本身）
    next_tasks = task_list[idx:]
    if not next_tasks:
        session.close()
        raise HTTPException(status_code=400, detail="No downstream tasks to retry")

    # 构建新的chain
    signatures = []
    if next_tasks:
        signatures.append(celery_app.signature(next_tasks[0], args=(event,)))
        for t in next_tasks[1:]:
            signatures.append(celery_app.signature(t))
    workflow = chain(*signatures)
    result = workflow.apply_async()
    session.close()
    return result.id