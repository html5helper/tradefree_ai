from celery.signals import task_prerun, task_postrun, task_failure, task_retry, task_revoked, task_sent
from sqlalchemy.orm import sessionmaker
from ai.core.history.task_event import TaskEvent, engine
from datetime import datetime
import json

Session = sessionmaker(bind=engine)

def parse_params(event):
    """解析任务参数"""
    params = {
        'src_platform': event.get('reference_product_platform',''),
        'src_product': event.get('reference_product',event.get('prodid','')),
        'dest_shop': event.get('published_shop',''),
        'workflow_name': event.get('workflow_name','')
    }
    return params

@task_sent.connect
def on_task_sent(sender=None, task_id=None, task=None, args=None, kwargs=None, **other):
    """任务创建时的初始状态"""
    session = Session()
    try:
        event = args[0] if args and isinstance(args[0], dict) else {}
        trace_id = event.get('trace_id')
        workflow_name = event.get('workflow_name')
        employee = event.get('employee','system')

        # params
        task_params = parse_params(event)
        
        task_event = TaskEvent(
            task_id=task_id,
            task_name=sender,
            task_owner=employee,
            task_input=args if args else None,
            task_kwargs=kwargs if kwargs else None,
            task_params=json.dumps(task_params),
            task_status='PENDING',
            trace_id=trace_id,
            workflow_name=workflow_name,
            created_at=datetime.utcnow()
        )
        session.add(task_event)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error recording task sent: {e}")
    finally:
        session.close()

@task_prerun.connect
def before_task_run(sender=None, task_id=None, task=None, args=None, kwargs=None, **other):
    """任务开始执行时的状态"""
    session = Session()
    try:
        history = session.query(TaskEvent).filter_by(task_id=task_id).first()
        if history:
            history.task_status = 'STARTED'
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error recording task prerun: {e}")
    finally:
        session.close()

@task_postrun.connect
def after_task_run(sender=None, task_id=None, retval=None, **other):
    session = Session()
    history = session.query(TaskEvent).filter_by(task_id=task_id).first()
    if history:
        history.task_status = 'SUCCESS'
        if isinstance(retval, dict):
            history.task_output = json.dumps(retval)
        else:
            history.task_output = str(retval)
        history.finished_at = datetime.utcnow()
        session.commit()
    session.close()

@task_failure.connect
def on_task_failure(sender=None, task_id=None, **other):
    session = Session()
    history = session.query(TaskEvent).filter_by(task_id=task_id).first()
    if history:
        history.task_status = 'FAILURE'
        history.finished_at = datetime.utcnow()
        session.commit()
    session.close()

@task_retry.connect
def on_task_retry(sender=None, task_id=None, **other):
    session = Session()
    history = session.query(TaskEvent).filter_by(task_id=task_id).first()
    if history:
        history.task_status = 'RETRY'
        session.commit()
    session.close()

@task_revoked.connect
def on_task_revoked(sender=None, task_id=None, **other):
    session = Session()
    history = session.query(TaskEvent).filter_by(task_id=task_id).first()
    if history:
        history.task_status = 'REVOKED'
        history.finished_at = datetime.utcnow()
        session.commit()
    session.close()
