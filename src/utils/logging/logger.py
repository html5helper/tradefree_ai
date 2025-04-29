import logging
import os
from datetime import datetime

# 创建日志目录
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志格式
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# 创建日志记录器
def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(console_handler)
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f"{log_file}_{datetime.now().strftime('%Y%m%d')}.log")
        )
        file_handler.setFormatter(logging.Formatter(log_format, date_format))
        logger.addHandler(file_handler)
    
    return logger

# 创建各个模块的日志记录器
event_logger = setup_logger("event", "event")
task_logger = setup_logger("task", "task")
workflow_logger = setup_logger("workflow", "workflow")
api_logger = setup_logger("api", "api") 