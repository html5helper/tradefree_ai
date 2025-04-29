# 项目目录结构

```
tradefree_ai/
├── README.md                 # 项目说明文档
├── architecture.md           # 架构设计文档
├── install.sh               # 安装脚本
├── run.sh                   # 运行脚本
├── requirements.txt         # Python依赖
├── config/                  # 配置文件目录
│   ├── config.py           # 主配置文件
│   └── logging.conf        # 日志配置
├── src/                     # 源代码目录
│   ├── __init__.py
│   ├── main.py             # 主程序入口
│   ├── api/                # API接口
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/               # 核心功能
│   │   ├── __init__.py
│   │   ├── task.py        # 任务模型
│   │   └── service.py     # 服务层
│   ├── dao/                # 数据访问层
│   │   ├── __init__.py
│   │   └── task_dao.py
│   ├── tasks/              # Celery任务
│   │   ├── __init__.py
│   │   └── worker.py
│   └── utils/              # 工具函数
│       ├── __init__.py
│       └── logger.py
├── tests/                   # 测试目录
│   ├── __init__.py
│   ├── test_task.py
│   └── test_service.py
├── logs/                    # 日志目录
└── scripts/                 # 脚本目录
    ├── setup_db.sh         # 数据库初始化脚本
    └── backup.sh           # 备份脚本
``` 