from sqlalchemy.orm import Session
from ai.dao.db.engine import workflow_engine
from ai.dao.entity.task_event import TaskEvent

class TaskEventService:
    def __init__(self):
        self.session = None

    def _get_session(self):
        """获取数据库会话"""
        if self.session is None:
            self.session = Session(bind=workflow_engine)
        return self.session

    def add(self, task_event: TaskEvent) -> bool:
        """添加任务事件
        
        Args:
            task_event: 任务事件
            
        Returns:
            bool: 是否添加成功
        """
        session = self._get_session()
        try:
            session.add(task_event)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error adding task event: {str(e)}")
            return False

    def get(self, task_id: str) -> TaskEvent:
        """获取任务事件
        
        Args:
            task_id: 任务ID
            
        Returns:
            TaskEvent: 任务事件
        """
        session = self._get_session()
        try:
            result = session.query(TaskEvent).filter_by(task_id=task_id).first()
            return result
        except Exception as e:
            print(f"Error getting task event: {str(e)}")
            return None

    def update(self, task_id: str, changes: dict) -> TaskEvent:
        """更新任务事件
        
        Args:
            task_id: 任务ID
            changes: 更新内容
            
        Returns:
            TaskEvent: 更新后的任务事件，如果更新失败则返回None
        """
        session = self._get_session()
        try:
            task_event = session.query(TaskEvent).filter_by(task_id=task_id).first()
            if task_event:
                for key, value in changes.items():
                    setattr(task_event, key, value)
                session.commit()
                return task_event
            return None
        except Exception as e:
            session.rollback()
            print(f"Error updating task event: {str(e)}")
            return None

    def close_session(self):
        """关闭数据库会话"""
        if self.session:
            self.session.close()
            self.session = None

    def __del__(self):
        """确保session被正确关闭"""
        self.close_session() 