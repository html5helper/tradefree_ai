from celery import Celery
import os
import importlib

# 创建Celery应用，指定配置模块
app = Celery('myapp')
app.config_from_object('ai.config.celeryconfig')

def discover_task_modules():
    """自动发现ai/business目录下的所有任务模块"""
    task_modules = []
    business_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'business')
    
    # 遍历business目录下的所有子目录
    for item in os.listdir(business_dir):
        item_path = os.path.join(business_dir, item)
        # 检查是否是目录且包含tasks.py文件
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'tasks.py')):
            module_name = f'ai.business.{item}'
            # 尝试导入模块以验证其有效性
            try:
                importlib.import_module(module_name)
                task_modules.append(module_name)
            except ImportError:
                continue
    
    return task_modules

# 自动发现任务模块
app.autodiscover_tasks(discover_task_modules())

# 引入监听器来记录任务历史到MYSQL的task_history表
import ai.core.history.task_listener