# Tradefree AI 任务系统架构设计

## 1. 系统概述

### 1.1 核心功能
- 事件触发任务执行
- 任务并行度控制
- 任务状态监控
- 执行日志查看

### 1.2 技术栈
- 任务队列：Celery
- AI 服务：Dify
- 消息队列：Redis
- 数据库：MySQL
- 监控：基础日志系统

## 2. 系统架构

### 2.1 整体架构
```
[外部系统/用户] 
      ↓
[任务管理服务] ──── [Redis] ──── [Celery Workers]
      ↓                                    ↓
[Dify API] ─────────────────────────── [MySQL]
```

### 2.2 核心服务

1. **任务管理服务**
   - 功能：任务接收、分发、状态管理
   - 技术：Python + FastAPI
   - 部署：单实例部署

2. **任务执行服务**
   - 功能：任务执行、重试、结果处理
   - 技术：Python + Celery
   - 部署：Worker 集群

3. **数据存储**
   - 功能：任务状态、执行结果
   - 技术：MySQL + Redis
   - 部署：单实例

## 3. 数据模型设计

### 3.1 数据库表结构

```sql
-- 任务表
CREATE TABLE tasks (
    id VARCHAR(36) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    input_data JSON,
    output_data JSON,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 任务日志表
CREATE TABLE task_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL,
    level VARCHAR(20) NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_task_id (task_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3.2 数据模型类

```python
# 任务模型
class Task:
    id: str                    # 任务ID
    type: str                  # 任务类型
    status: str                # 状态
    input_data: dict           # 输入数据
    output_data: dict          # 输出数据
    created_at: datetime       # 创建时间
    updated_at: datetime       # 更新时间
    error_message: str         # 错误信息

# 任务日志模型
class TaskLog:
    id: int                    # 日志ID
    task_id: str               # 任务ID
    level: str                 # 日志级别
    message: str               # 日志消息
    created_at: datetime       # 创建时间
```

## 4. 数据访问层

### 4.1 数据库连接配置

```python
# config.py
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'tradefree',
    'password': 'password',
    'database': 'tradefree_ai',
    'charset': 'utf8mb4'
}
```

### 4.2 数据访问类

```python
# dao.py
import pymysql
from contextlib import contextmanager

class TaskDAO:
    @contextmanager
    def get_connection(self):
        conn = pymysql.connect(**DB_CONFIG)
        try:
            yield conn
        finally:
            conn.close()

    def create_task(self, task: Task) -> str:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO tasks (id, type, status, input_data, output_data)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    task.id,
                    task.type,
                    task.status,
                    json.dumps(task.input_data),
                    json.dumps(task.output_data)
                ))
                conn.commit()
                return task.id

    def update_task_status(self, task_id: str, status: str, output_data: dict = None):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                if output_data:
                    sql = """
                    UPDATE tasks 
                    SET status = %s, output_data = %s 
                    WHERE id = %s
                    """
                    cursor.execute(sql, (status, json.dumps(output_data), task_id))
                else:
                    sql = """
                    UPDATE tasks 
                    SET status = %s 
                    WHERE id = %s
                    """
                    cursor.execute(sql, (status, task_id))
                conn.commit()

    def get_task(self, task_id: str) -> Task:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM tasks WHERE id = %s"
                cursor.execute(sql, (task_id,))
                row = cursor.fetchone()
                if row:
                    return Task(
                        id=row['id'],
                        type=row['type'],
                        status=row['status'],
                        input_data=json.loads(row['input_data']),
                        output_data=json.loads(row['output_data']),
                        created_at=row['created_at'],
                        updated_at=row['updated_at'],
                        error_message=row['error_message']
                    )
                return None
```

## 5. 任务执行流程

### 5.1 任务创建
```python
# task_service.py
class TaskService:
    def __init__(self):
        self.task_dao = TaskDAO()
        self.celery = Celery()
        self.dify = DifyClient()

    async def create_task(self, task_type: str, input_data: dict) -> str:
        # 创建任务记录
        task = Task(
            id=str(uuid.uuid4()),
            type=task_type,
            status='pending',
            input_data=input_data,
            output_data={}
        )
        
        # 保存到数据库
        task_id = self.task_dao.create_task(task)
        
        # 发送到队列
        self.celery.send_task('process_task', args=[task_id])
        
        return task_id
```

### 5.2 任务处理
```python
# tasks.py
@app.task(bind=True, max_retries=3)
def process_task(self, task_id):
    try:
        # 获取任务
        task = task_dao.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
            
        # 更新状态
        task_dao.update_task_status(task_id, 'processing')
        
        # 执行任务
        result = dify.process(task.input_data)
        
        # 更新结果
        task_dao.update_task_status(task_id, 'completed', result)
        
        return result
    except Exception as e:
        # 更新错误状态
        task_dao.update_task_status(task_id, 'failed', error_message=str(e))
        raise
```

## 6. 监控和日志

### 6.1 日志记录
```python
# logger.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('tradefree_ai')
```

### 6.2 基础监控
```python
# monitor.py
class TaskMonitor:
    def __init__(self):
        self.task_dao = TaskDAO()
        
    def get_task_stats(self):
        with self.task_dao.get_connection() as conn:
            with conn.cursor() as cursor:
                # 获取任务统计
                sql = """
                SELECT 
                    status,
                    COUNT(*) as count
                FROM tasks
                GROUP BY status
                """
                cursor.execute(sql)
                return cursor.fetchall()
```

## 7. 部署架构

### 7.1 生产环境
```
[任务管理服务] ──── [Redis] ──── [Celery Workers]
      ↓                                    ↓
[MySQL] ─────────────────────────────── [日志文件]
```

### 7.2 扩缩容策略
- Worker 数量根据负载动态调整
- 数据库配置根据数据量调整

## 8. 安全设计

### 8.1 基础安全
1. **API 安全**
   - API Key 认证
   - 基础访问控制

2. **数据安全**
   - 数据备份
   - 访问控制

## 9. 开发规范

### 9.1 代码规范
- Python 基础规范
- 基础文档注释
- 错误处理规范

### 9.2 测试规范
- 基础单元测试
- 集成测试
- 手动测试流程

## 10. 实施建议

### 10.1 第一阶段
1. 搭建基础架构
2. 实现核心功能
3. 部署测试环境

### 10.2 第二阶段
1. 优化性能
2. 完善监控
3. 部署生产环境

### 10.3 第三阶段
1. 收集反馈
2. 优化体验
3. 扩展功能 