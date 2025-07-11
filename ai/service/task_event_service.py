from sqlalchemy.orm import Session
from ai.dao.db.engine import workflow_engine
from ai.dao.entity.task_event import TaskEvent

class TaskEventService:
    def __init__(self):
        self.session = Session(bind=workflow_engine)

    def add(self, task_event: TaskEvent) -> bool:
        """添加任务事件
        
        Args:
            task_event: 任务事件
            
        Returns:
            bool: 是否添加成功
        """
        try:
            self.session.add(task_event)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error adding task event: {str(e)}")
            return False
        finally:
            self.session.close()

    def get(self, task_id: str) -> dict:
        """获取任务事件
        
        Args:
            task_id: 任务ID
            
        Returns:
            dict: 任务事件数据字典
        """
        try:
            result = self.session.query(TaskEvent).filter_by(task_id=task_id).first()
            if result:
                # 在Session关闭前转换为字典
                return result.to_dict()
            return None
        except Exception as e:
            print(f"Error getting task event: {str(e)}")
            return None
        finally:
            self.session.close()

    def update(self, task_id: str, changes: dict) -> dict:
        """更新任务事件
        
        Args:
            task_id: 任务ID
            changes: 更新内容
            
        Returns:
            dict: 更新后的任务事件数据字典，如果更新失败则返回None
        """
        try:
            task_event = self.session.query(TaskEvent).filter_by(task_id=task_id).first()
            if task_event:
                for key, value in changes.items():
                    if hasattr(task_event, key):
                        setattr(task_event, key, value)
                self.session.commit()
                # 在Session关闭前转换为字典
                return task_event.to_dict()
            return None
        except Exception as e:
            self.session.rollback()
            print(f"Error updating task event: {str(e)}")
            return None
        finally:
            self.session.close()

    def __del__(self):
        """确保session被正确关闭"""
        if hasattr(self, 'session'):
            self.session.close()