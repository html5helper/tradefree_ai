from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime
from .event import Event, event_manager
from utils.logging.logger import task_logger
from config.workflow_config import TASK_HANDLERS

@dataclass
class Task:
    """任务基类"""
    task_id: str
    task_type: str
    data: Dict[str, Any]
    created_at: datetime = datetime.now()
    status: str = "pending"

class TaskManager:
    """任务管理器"""
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_handlers: Dict[str, callable] = {}
        task_logger.info("任务管理器初始化完成")
        self.setup_task_handlers()

    def setup_task_handlers(self):
        """设置任务处理器"""
        # 注册任务处理器
        self.register_handler("worker_001", self.worker_001_handler)
        self.register_handler("worker_002", self.worker_002_handler)
        task_logger.info("任务处理器设置完成")

    def register_handler(self, task_type: str, handler: callable):
        """注册任务处理器"""
        self.task_handlers[task_type] = handler
        task_logger.info(f"注册任务处理器: {task_type}")

    def execute_task(self, task: Task):
        """执行任务"""
        self.tasks[task.task_id] = task
        task_logger.info(f"开始执行任务: {task.task_type}, ID: {task.task_id}")
        
        if task.task_type not in self.task_handlers:
            task_logger.error(f"未找到任务处理器: {task.task_type}")
            raise ValueError(f"未找到任务处理器: {task.task_type}")
            
        try:
            result = self.task_handlers[task.task_type](task)
            task.status = "completed"
            task_logger.info(f"任务执行成功: {task.task_type}, ID: {task.task_id}")
            return result
        except Exception as e:
            task.status = "failed"
            task_logger.error(f"任务执行失败: {task.task_type}, ID: {task.task_id}, 错误: {str(e)}")
            raise e

    def worker_001_handler(self, task: Task):
        """worker_001 处理器"""
        task_logger.info(f"执行 worker_001: {task.data}")
        # 任务完成后触发 event_002
        event = Event(
            event_id=f"event_002_{datetime.now().timestamp()}",
            event_type="event_002",
            data={
                "message": "worker_001 completed",
                "timestamp": datetime.now().isoformat()
            }
        )
        event_manager.trigger_event(event)
        return {"status": "success", "message": "worker_001 completed"}

    def worker_002_handler(self, task: Task):
        """worker_002 处理器"""
        task_logger.info(f"执行 worker_002: {task.data}")
        return {"status": "success", "message": "worker_002 completed"}

# 创建全局任务管理器实例
task_manager = TaskManager()