from typing import Dict, Any, List
from .event import Event, event_manager
from .task import Task, task_manager
from utils.logging.logger import workflow_logger
from config.workflow_config import WORKFLOW_CONFIGS, TASK_HANDLERS, EVENT_HANDLERS

class Workflow:
    """工作流定义"""
    def __init__(self, workflow_id: str):
        if workflow_id not in WORKFLOW_CONFIGS:
            raise ValueError(f"工作流配置不存在: {workflow_id}")
            
        self.workflow_id = workflow_id
        self.config = WORKFLOW_CONFIGS[workflow_id]
        self.setup_event_handlers()
        workflow_logger.info(f"工作流初始化完成: {workflow_id}")

    def setup_event_handlers(self):
        """设置事件处理器"""
        for event_type in self.config["events"]:
            if event_type in EVENT_HANDLERS:
                event_manager.register_handler(event_type, getattr(self, f"handle_{event_type}"))
                workflow_logger.info(f"注册事件处理器: {event_type}")
            else:
                workflow_logger.warning(f"未找到事件处理器配置: {event_type}")
        workflow_logger.info("事件处理器设置完成")

    def handle_event_001(self, event: Event):
        """处理 event_001"""
        workflow_logger.info(f"处理 event_001: {event.data}")
        # 验证必要字段
        self._validate_event_data(event, "event_001")
        
        # 创建并执行 worker_001 任务
        task = Task(
            task_id=f"worker_001_{event.event_id}",
            task_type="worker_001",
            data=event.data
        )
        task_manager.execute_task(task)

    def handle_event_002(self, event: Event):
        """处理 event_002"""
        workflow_logger.info(f"处理 event_002: {event.data}")
        # 验证必要字段
        self._validate_event_data(event, "event_002")
        
        # 创建并执行 worker_002 任务
        task = Task(
            task_id=f"worker_002_{event.event_id}",
            task_type="worker_002",
            data=event.data
        )
        task_manager.execute_task(task)

    def _validate_event_data(self, event: Event, event_type: str):
        """验证事件数据"""
        required_fields = EVENT_HANDLERS[event_type]["required_fields"]
        for field in required_fields:
            if field not in event.data:
                raise ValueError(f"事件数据缺少必要字段: {field}")

# 创建工作流实例
workflow = Workflow("hello_world")