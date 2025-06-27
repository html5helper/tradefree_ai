from celery.signals import task_prerun, task_postrun, task_failure, task_retry, task_revoked, task_sent
from ai.dao.entity.task_event import TaskEvent
from ai.service.task_event_service import TaskEventService
from datetime import datetime
import json

task_event_service = TaskEventService()

class TaskEventHook:
    """任务事件钩子
    Args:
        task_event_data: 任务事件数据
        employee_info: 员工信息
        product_info: 产品信息

    Returns:
        TaskEvent: 任务事件
    """
    """ 任务状态说明：
        - PENDING: 任务已创建，等待执行
        - STARTED: 任务已开始执行
        - SUCCESS: 任务执行成功，发品成功
        - FAILURE: 任务执行失败，发品失败
        - RETRY: 任务正在重试
        - REVOKED: 任务已被撤销
    """
    def __init__(self):
        pass

    def pending(self, task_id: str, task_name: str, task_input: dict) -> TaskEvent:
        """任务事件初始状态"""
        task_event = self.parse_task_event(task_id, task_name, task_input)
        if task_event:
            # 先保存到数据库，确保实例绑定到Session
            success = task_event_service.add(task_event)
            if success:
                # 重新获取实例，确保它绑定到Session
                return task_event_service.get(task_id)
        return None
    
    def started(self, task_id: str, task_name: str, task_input: dict) -> TaskEvent:
        """任务事件执行中状态"""
        try:
            task_event = task_event_service.get(task_id)
            
            if task_event is not None:
                task_event = task_event_service.update(task_id, {'task_status': 'STARTED'})
                return task_event
            else:
                return None
            
        except Exception as e:
            print(f"Error recording task prerun: {e}")
            return None
    
    def success(self, task_id: str, task_name: str, task_input: dict,task_output: dict) -> TaskEvent:
        """任务事件执行成功状态"""
        try:
            # 更新任务事件状态
            task_event = task_event_service.update(task_id, {
                    'task_status': 'SUCCESS', 
                    'task_output': json.dumps(task_output), 
                    'finished_at': datetime.utcnow()
                })
            return task_event
        except Exception as e:
            print(f"Error recording task success: {e}")
            return None
    
    def failure(self, task_id: str, task_name: str) -> TaskEvent:
        """任务事件执行失败状态"""
        try:
            task_event = task_event_service.update(task_id, {
                    'task_status': 'FAILURE', 
                    'finished_at': datetime.utcnow()
                })
            return task_event
        except Exception as e:
            print(f"Error recording task failure: {e}")
            return None
    
    def revoked(self, task_id: str, task_name: str, task_input: dict,task_output: dict) -> TaskEvent:
        """任务事件撤销状态"""
        try:
            task_event = task_event_service.update(task_id, {
                    'task_status': 'REVOKED',
                    'finished_at': datetime.utcnow()
                })
            return task_event
        except Exception as e:
            print(f"Error recording task revoked: {e}")
            return None
    
    def retry(self, task_id: str, task_name: str) -> TaskEvent:
        """任务事件重试状态"""
        try:
            task_event = task_event_service.update(task_id, {
                    'task_status': 'RETRY'
                })
            return task_event
        except Exception as e:
            print(f"Error recording task retry: {e}")
            return None

    def parse_task_event(self,task_id: str, task_name: str, task_input: dict) -> TaskEvent:
        """解析任务事件"""
        try:
            access = task_input.get('access',{})

            trace_id = task_input.get('trace_id')
            workflow_name = task_input.get('workflow')
            task_owner = access.get('employee_name','system')
            # 取task_type = 从前往后的第三部分
            task_type = task_name.split('.')[2]
            
            # 安全地提取 dest_platform
            if workflow_name and '_' in workflow_name:
                parts = workflow_name.split('_')
                dest_platform = parts[2] if len(parts) > 2 else '--'
            else:
                dest_platform = '--'
            
            task_event = TaskEvent(
                task_id=task_id,
                task_name=task_name,
                task_owner=task_owner,
                task_type=task_type,
                task_input=json.dumps(task_input),
                task_status='PENDING',
                trace_id=trace_id,
                workflow_name=workflow_name,
                dest_platform=dest_platform,
                created_at=datetime.utcnow()
            )
            return task_event
        except Exception as e:
            print(f"Error parsing task event: {e}")
            return None
        