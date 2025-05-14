from ai.core.celery_app import app as celery_app
from celery import chain
from ai.core.history.task_history import TaskHistory, engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

Session = sessionmaker(bind=engine)

def retry_chain_by_task_id(task_id: str):
    session = Session()
    history = session.query(TaskHistory).filter_by(task_id=task_id).first()
    if not history:
        session.close()
        raise HTTPException(status_code=404, detail="Task history not found")
    task_name = history.name
    args = history.args or []
    event = args[0] if args else None
    if not event:
        session.close()
        raise HTTPException(status_code=400, detail="No event found in args")

    # 定义各类chain的任务顺序
    chain_map = {
        "amz_to_ali": [
            'ai.business.resource.tasks.amz_to_ali_src',
            'ai.business.listing.tasks.amz_to_ali_listing',
            'ai.business.image.tasks.amz_to_ali_image',
            'ai.business.upload_img.tasks.amz_to_ali_upload',
            'ai.business.public.tasks.amz_to_ali_public',
        ],
        "amz_to_1688": [
            'ai.business.resource.tasks.amz_to_1688_src',
            'ai.business.listing.tasks.amz_to_1688_listing',
            'ai.business.image.tasks.amz_to_1688_image',
            'ai.business.upload_img.tasks.amz_to_1688_upload',
            'ai.business.public.tasks.amz_to_1688_public',
        ],
        "1688_to_1688": [
            'ai.business.resource.tasks._1688_to_1688_src',
            'ai.business.listing.tasks._1688_to_1688_listing',
            'ai.business.image.tasks._1688_to_1688_image',
            'ai.business.upload_img.tasks._1688_to_1688_upload',
            'ai.business.public.tasks._1688_to_1688_public',
        ],
        "ali_to_ali": [
            'ai.business.resource.tasks.ali_to_ali_src',
            'ai.business.listing.tasks.ali_to_ali_listing',
            'ai.business.image.tasks.ali_to_ali_image',
            'ai.business.upload_img.tasks.ali_to_ali_upload',
            'ai.business.public.tasks.ali_to_ali_public',
        ],
    }

    # 判断属于哪个chain
    chain_type = None
    for key in chain_map:
        if key in task_name:
            chain_type = key
            break
    if not chain_type:
        session.close()
        raise HTTPException(status_code=400, detail="Unsupported chain for this task")

    task_list = chain_map[chain_type]
    # 找到失败任务在chain中的位置
    try:
        idx = task_list.index(task_name)
    except ValueError:
        session.close()
        raise HTTPException(status_code=400, detail="Task name not found in chain definition")

    # 只取失败任务之后的任务
    next_tasks = task_list[idx:]
    if not next_tasks:
        session.close()
        raise HTTPException(status_code=400, detail="No downstream tasks to retry")

    # 构建新的chain
    signatures = []
    # 第一个未完成任务需要带event参数
    if next_tasks:
        signatures.append(celery_app.signature(next_tasks[0], args=(event,)))
        for t in next_tasks[1:]:
            signatures.append(celery_app.signature(t))
    workflow = chain(*signatures)
    result = workflow.apply_async()
    session.close()
    return result.id
