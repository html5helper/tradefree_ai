"""工作流配置文件"""
from typing import Dict, Any, List

# 工作流配置
WORKFLOW_CONFIGS: Dict[str, Dict[str, Any]] = {
    "hello_world": {
        "name": "Hello World 工作流",
        "description": "示例工作流",
        "events": ["event_001", "event_002"],
        "tasks": ["worker_001", "worker_002"],
        "version": "1.0.0"
    }
}

# 事件处理器配置
EVENT_HANDLERS: Dict[str, Dict[str, Any]] = {
    "event_001": {
        "name": "事件001处理器",
        "description": "处理事件001的逻辑",
        "required_fields": ["message", "timestamp"],
        "task_mapping": "worker_001"
    },
    "event_002": {
        "name": "事件002处理器",
        "description": "处理事件002的逻辑",
        "required_fields": ["message", "timestamp"],
        "task_mapping": "worker_002"
    }
}

# 任务处理器配置
TASK_HANDLERS: Dict[str, Dict[str, Any]] = {
    "worker_001": {
        "name": "任务001处理器",
        "description": "执行任务001的逻辑",
        "required_fields": ["message", "timestamp"],
        "timeout": 300,  # 超时时间（秒）
        "retry": {
            "max_attempts": 3,
            "delay": 60  # 重试延迟（秒）
        }
    },
    "worker_002": {
        "name": "任务002处理器",
        "description": "执行任务002的逻辑",
        "required_fields": ["message", "timestamp"],
        "timeout": 300,
        "retry": {
            "max_attempts": 3,
            "delay": 60
        }
    }
} 