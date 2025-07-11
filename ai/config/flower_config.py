# Flower 持久化配置

FLOWER_CONFIG = {
    'db': './data/flower/flower.db',  # 使用 SQLite 文件作为 Flower 持久化存储
    'persistent': True,  # 启用持久化
    'max_tasks': 10000,  # 最大任务数量
    'enable_events': True,  # 启用事件
    'auto_refresh': True,  # 自动刷新
    'auto_refresh_interval': 5000,  # 自动刷新间隔（毫秒）
    'task_events': True,  # 任务事件
    'worker_events': True,  # Worker 事件
    'task_ignore_result': False,  # 不忽略任务结果
    'task_track_started': True,  # 跟踪任务开始状态
    'page_size': 50,  # 页面大小
    'natural_time': True,  # 自然时间显示
} 