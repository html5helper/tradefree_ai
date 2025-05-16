from celery.signals import task_prerun, task_postrun, task_failure
from sqlalchemy.orm import sessionmaker
from ai.core.history.task_event import TaskEvent, engine
from datetime import datetime
import json

Session = sessionmaker(bind=engine)

@task_prerun.connect
def before_task_run(sender=None, task_id=None, task=None, args=None, kwargs=None, **other):
    session = Session()
    try:
        event = args[0] if args and isinstance(args[0], dict) else {}
        trace_id = event.get('trace_id')
        workflow_name = event.get('workflow_name')
        task_event = TaskEvent(
            task_id=task_id,
            task_name=sender.name,
            task_input=args if args else None,
            task_kwargs=kwargs if kwargs else None,
            task_status='STARTED',
            trace_id=trace_id,
            workflow_name=workflow_name,
            created_at=datetime.utcnow()
        )
        session.add(task_event)
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
