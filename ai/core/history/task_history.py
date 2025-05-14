from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

engine = create_engine(
    "mysql+pymysql://root:c1234%^5678C@localhost:3306/celery?charset=utf8mb4",
    echo=True
)

# CREATE TABLE `task_history` (
#     `id` INT AUTO_INCREMENT PRIMARY KEY,
#     `task_id` VARCHAR(255) NOT NULL UNIQUE,
#     `task_name` VARCHAR(255) NOT NULL,
#     `args` JSON,
#     `kwargs` JSON,
#     `status` VARCHAR(50),
#     `trace_id` VARCHAR(255),
#     `workflow_name` VARCHAR(255),
#     `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
#     `finished_at` DATETIME,
#     INDEX `idx_trace_id` (`trace_id`),
#     INDEX `idx_workflow_name` (`workflow_name`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

class TaskHistory(Base):
    __tablename__ = "task_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(255), unique=True, nullable=False)
    task_name = Column(String(255), nullable=False)
    args = Column(JSON)
    kwargs = Column(JSON)
    status = Column(String(50))
    trace_id = Column(String(255), index=True)
    workflow_name = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)

    def __repr__(self):
        return f"<TaskHistory(task_id='{self.task_id}', task_name='{self.task_name}', status='{self.status}')>"