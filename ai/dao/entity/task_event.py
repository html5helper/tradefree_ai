from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# CREATE TABLE `task_event` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `task_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `task_owner` VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `task_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `task_input` json DEFAULT NULL,
#   `task_output` text COLLATE utf8mb4_unicode_ci,
#   `task_status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `trace_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `workflow_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `dest_platform` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `retried` TINYINT DEFAULT 0,
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
#   `finished_at` datetime DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `task_id` (`task_id`),
#   KEY `idx_trace_id` (`trace_id`),
#   KEY `idx_workflow_name` (`workflow_name`)
# ) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

class TaskEvent(Base):
    """任务事件模型
    
    任务状态说明：
    - PENDING: 任务已创建，等待执行
    - STARTED: 任务已开始执行
    - SUCCESS: 任务执行成功
    - FAILURE: 任务执行失败
    - RETRY: 任务正在重试
    - REVOKED: 任务已被撤销
    """
    __tablename__ = "task_event"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(255), unique=True, nullable=False)
    task_name = Column(String(255), nullable=False)
    task_owner = Column(String(255), nullable=False)
    task_type = Column(String(255), nullable=False)
    task_input = Column(JSON)
    task_output = Column(Text)
    task_status = Column(String(50))  # PENDING: 等待执行, STARTED: 已开始执行, SUCCESS: 执行成功, FAILURE: 执行失败, RETRY: 重试中, REVOKED: 已撤销
    trace_id = Column(String(255), index=True)
    workflow_name = Column(String(255), index=True)
    dest_platform = Column(String(255), nullable=False)
    retried = Column(Integer, default=0, nullable=False)  # 0: 未重试, 1: 已重试
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)

    def __repr__(self):
        try:
            return f"<TaskEvent(task_id='{self.task_id}', task_name='{self.task_name}', task_owner='{self.task_owner}', status='{self.task_status}')>"
        except:
            # 如果对象是 detached 状态，返回简单的表示
            return f"<TaskEvent(id={getattr(self, 'id', 'N/A')})>"
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_owner': self.task_owner,
            'task_type': self.task_type,
            'task_status': self.task_status,
            'task_input': self.task_input,
            'task_output': self.task_output,
            'trace_id': self.trace_id,
            'workflow_name': self.workflow_name,
            'dest_platform': self.dest_platform,
            'retried': self.retried,
            'created_at': self.created_at,
            'finished_at': self.finished_at,
        }