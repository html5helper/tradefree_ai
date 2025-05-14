from celery.signals import task_prerun, task_postrun, task_failure, task_sent, task_received, task_success, task_retry
from sqlalchemy.orm import sessionmaker
from ai.core.history.task_history import TaskHistory, engine
from datetime import datetime
import json

Session = sessionmaker(bind=engine)

@task_sent.connect
def task_sent_handler(sender=None, headers=None, **kwargs):
    session = Session()
    try:
        args = headers.get('args', [])
        event = args[0] if args and isinstance(args[0], dict) else None
        trace_id = event.get('trace_id') if isinstance(event, dict) else None
        workflow_name = event.get('workflow_name') if isinstance(event, dict) else None

        task = TaskHistory(
            task_id=headers.get('id'),
            task_name=headers.get('task'),
            args=args if args else None,
            kwargs=headers.get('kwargs', {}),
            status='PENDING',
            trace_id=trace_id,
            workflow_name=workflow_name,
            created_at=datetime.utcnow()
        )
        session.add(task)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error recording task sent: {e}")
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
