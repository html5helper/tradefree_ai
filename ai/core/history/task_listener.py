from celery.signals import task_prerun, task_postrun, task_failure, task_sent, task_received, task_success, task_retry
from sqlalchemy.orm import sessionmaker
from ai.core.history.task_history import TaskHistory, engine
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
        task_history = TaskHistory(
            task_id=task_id,
            task_name=sender.name,
            args=args if args else None,
            kwargs=kwargs if kwargs else None,
            status='STARTED',
            trace_id=trace_id,
            workflow_name=workflow_name,
            created_at=datetime.utcnow()
        )
        session.add(task_history)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error recording task prerun: {e}")
    finally:
        session.close()

@task_postrun.connect
def after_task_run(sender=None, task_id=None, **other):
    session = Session()
    history = session.query(TaskHistory).filter_by(task_id=task_id).first()
    if history:
        history.status = 'SUCCESS'
        history.finished_at = datetime.utcnow()
        session.commit()
    session.close()

@task_failure.connect
def on_task_failure(sender=None, task_id=None, **other):
    session = Session()
    history = session.query(TaskHistory).filter_by(task_id=task_id).first()
    if history:
        history.status = 'FAILURE'
        history.finished_at = datetime.utcnow()
        session.commit()
    session.close()
