from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
from utils.logging.logger import event_logger

@dataclass
class Event:
    """事件基类"""
    event_id: str
    event_type: str
    data: Dict[str, Any]
    created_at: datetime = datetime.now()
    status: str = "pending"

class EventManager:
    """事件管理器"""
    def __init__(self):
        self.events: Dict[str, Event] = {}
        self.event_handlers: Dict[str, List[callable]] = {}
        event_logger.info("事件管理器初始化完成")

    def register_handler(self, event_type: str, handler: callable):
        """注册事件处理器"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        event_logger.info(f"注册事件处理器: {event_type}")

    def trigger_event(self, event: Event):
        """触发事件"""
        self.events[event.event_id] = event
        event_logger.info(f"触发事件: {event.event_type}, ID: {event.event_id}")
        if event.event_type in self.event_handlers:
            for handler in self.event_handlers[event.event_type]:
                try:
                    handler(event)
                    event_logger.info(f"事件处理成功: {event.event_type}, ID: {event.event_id}")
                except Exception as e:
                    event_logger.error(f"事件处理失败: {event.event_type}, ID: {event.event_id}, 错误: {str(e)}")
                    raise e
        else:
            event_logger.warning(f"未找到事件处理器: {event.event_type}")

# 创建全局事件管理器实例
event_manager = EventManager()