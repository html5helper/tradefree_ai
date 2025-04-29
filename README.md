# Tradefree AI

基于 AI 的交易系统，支持工作流自动化和任务管理。

## 项目结构

```
tradefree_ai/
├── src/                    # 源代码目录
│   ├── core/              # 核心业务逻辑
│   │   ├── workflow_engine.py    # 工作流引擎和管理
│   │   ├── event.py       # 事件处理系统
│   │   └── task.py        # 任务执行和调度
│   ├── providers/         # AI 服务提供商实现
│   │   ├── base.py        # 提供商基础接口
│   │   ├── openai.py      # OpenAI 提供商实现
│   │   └── anthropic.py   # Anthropic 提供商实现
│   ├── tasks/             # Celery 任务
│   │   ├── worker.py      # Celery 工作进程配置
│   │   ├── tasks.py       # 任务定义
│   │   └── schedules.py   # 任务调度
│   ├── utils/             # 工具函数
│   │   ├── logging/      # 日志配置
│   │   │   └── logger.py # 日志设置和配置
│   │   ├── security/     # 安全工具
│   │   │   └── auth.py   # 认证和授权
│   │   └── helpers/      # 辅助函数
│   │       ├── time.py   # 时间相关工具
│   │       └── data.py   # 数据处理工具
│   ├── models/           # 数据模型
│   │   ├── database/    # 数据库模型
│   │   │   ├── base.py  # 基础数据库模型
│   │   │   └── models.py # SQLAlchemy 模型
│   │   └── ai/          # AI 模型定义
│   │       └── models.py # AI 模型配置
│   └── api/             # API 实现
│       ├── routes/      # API 路由
│       │   ├── events.py # 事件相关接口
│       │   ├── tasks.py  # 任务相关接口
│       │   └── workflow_api.py # 工作流相关接口
│       └── middleware/  # API 中间件
│           ├── auth.py  # 认证中间件
│           └── error.py # 错误处理中间件
├── tests/                # 测试套件
│   ├── unit/            # 单元测试
│   │   ├── core/       # 核心模块测试
│   │   ├── providers/  # 提供商测试
│   │   └── utils/      # 工具测试
│   └── integration/     # 集成测试
│       └── api/        # API 集成测试
├── docs/                # 文档
│   ├── api/            # API 文档
│   │   └── endpoints.md # API 接口文档
│   └── architecture/   # 架构文档
│       └── design.md   # 系统设计文档
├── config/             # 配置文件
│   ├── development/   # 开发环境配置
│   │   └── config.py  # 开发环境设置
│   └── production/    # 生产环境配置
│       └── config.py  # 生产环境设置
├── logs/              # 日志文件
│   ├── api/          # API 日志
│   ├── worker/       # 工作进程日志
│   └── error/        # 错误日志
├── data/             # 数据存储
│   ├── raw/         # 原始数据
│   └── processed/   # 处理后的数据
├── dags/            # 工作流定义
│   ├── base.py      # 基础工作流定义
│   └── workflows/   # 具体工作流实现
├── scripts/         # 工具脚本
│   ├── install.sh   # 安装脚本
│   ├── run.sh       # 服务启动脚本
│   ├── setup_db.sh  # 数据库初始化脚本
│   └── backup.sh    # 备份脚本
└── venv/           # 虚拟环境
```

## 目录说明

### src/
- **core/**: 包含系统的核心业务逻辑
  - `workflow_engine.py`: 管理工作流执行和状态
  - `event.py`: 处理事件处理和触发
  - `task.py`: 管理任务执行和调度

- **providers/**: AI 服务提供商实现
  - `base.py`: 定义 AI 提供商接口
  - `openai.py`: OpenAI API 实现
  - `anthropic.py`: Anthropic API 实现

- **tasks/**: Celery 任务定义和配置
  - `worker.py`: Celery 工作进程设置和配置
  - `tasks.py`: 任务定义和实现
  - `schedules.py`: 任务调度配置

- **utils/**: 工具函数和辅助功能
  - `logging/`: 日志配置和设置
  - `security/`: 安全相关工具
  - `helpers/`: 通用辅助函数

- **models/**: 数据模型和模式
  - `database/`: 使用 SQLAlchemy 的数据库模型
  - `ai/`: AI 模型配置和定义

- **api/**: API 实现
  - `routes/`: API 接口定义
  - `middleware/`: API 中间件组件

### tests/
- **unit/**: 单个组件的单元测试
- **integration/**: 系统组件的集成测试

### docs/
- **api/**: API 文档
- **architecture/**: 系统架构文档

### config/
- **development/**: 开发环境配置
- **production/**: 生产环境配置

### logs/
- **api/**: API 请求和响应日志
- **worker/**: 工作进程日志
- **error/**: 错误和异常日志

### data/
- **raw/**: 原始数据存储
- **processed/**: 处理后的数据存储

### dags/
- 工作流定义和配置
- 基础工作流模板
- 具体工作流实现

### scripts/
- 安装、设置和维护的工具脚本
  - `install.sh`: 安装和设置脚本
  - `run.sh`: 服务启动脚本
  - `setup_db.sh`: 数据库初始化脚本
  - `backup.sh`: 备份和恢复脚本

## 安装说明

1. 安装依赖：
```bash
./install.sh
```

2. 启动服务：
```bash
source venv/bin/activate
./run.sh
```

## 开发规范

- 使用虚拟环境进行开发
- 遵循 PEP 8 代码风格指南
- 为新功能编写测试
- 更新相关文档
- 使用类型提示提高代码可维护性
- 遵循已建立的目录结构添加新组件