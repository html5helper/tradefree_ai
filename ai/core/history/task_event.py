from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ai.config.celeryconfig import MYSQL_CONFIG
Base = declarative_base()

mysql_url = (
    f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}"
    f"@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}?charset={MYSQL_CONFIG['charset']}"
)
engine = create_engine(mysql_url,echo=True)


# CREATE TABLE `task_event` (
#     `id` INT AUTO_INCREMENT PRIMARY KEY,
#     `task_id` VARCHAR(255) NOT NULL UNIQUE,
#     `task_name` VARCHAR(255) NOT NULL,
#     `task_input` JSON,
#     `task_kwargs` JSON,
#     `task_output` TEXT,
#     `task_status` VARCHAR(50),
#     `trace_id` VARCHAR(255),
#     `workflow_name` VARCHAR(255),
#     `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
#     `finished_at` DATETIME,
#     INDEX `idx_trace_id` (`trace_id`),
#     INDEX `idx_workflow_name` (`workflow_name`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

class TaskEvent(Base):
    __tablename__ = "task_event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(255), unique=True, nullable=False)
    task_name = Column(String(255), nullable=False)
    task_input = Column(JSON)
    task_kwargs = Column(JSON)
    task_output = Column(Text)
    task_status = Column(String(50))
    trace_id = Column(String(255), index=True)
    workflow_name = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)

    def __repr__(self):
        return f"<TaskEvent(task_id='{self.task_id}', task_name='{self.task_name}', status='{self.status}')>"