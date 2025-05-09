# 基于celery构建一个事件驱动的工作流系统
## 要求：
1. 所有的任务都通过Event进行驱动
2. 任务以可配置的方式组织为工作流，同一个工作流中的任务实例通过trace_id关联
3. 工作流支持DAG配置，其最小组成元素为Celery的Task
4. 通过API的方式触发工作流
5. 同一个event_type的任务，可设置任务并行度，没有执行的任务需在队列中等待
6. 任务Task需要有状态，且当前面的任务执行结束后才能执行新的任务
7. 工作流和任务执行的状态要可查看

# 设计&实现
为了构建一个基于 Celery 的事件驱动工作流系统，满足你所列出的要求，可以按照以下步骤进行设计和实现：
1. 事件驱动的任务
定义 Event 类：创建一个 Event 类，用于封装任务所需的数据和上下文信息。每个任务都应该能够接收一个 Event 对象，并根据其内容执行相应的操作。
2. 可配置的工作流
工作流配置：使用配置文件（如 YAML 或 JSON）或数据库来定义工作流。每个工作流可以被表示为一个有向无环图（DAG），其中节点代表任务。
使用 trace_id：在 Event 对象中包含 trace_id，用于关联同一工作流实例中的任务。
3. 支持 DAG 配置
Celery Canvas：利用 Celery 的 Canvas 功能（如链、组、和弦）来定义复杂的工作流。每个任务在 DAG 中都是一个 Celery 任务。
4. 通过 API 触发工作流
API 端点：实现一个 API 端点，用于接收启动工作流的请求。该端点应创建一个初始 Event 并触发工作流中的第一个任务。
5. 任务并行度
任务并行配置：配置 Celery 以允许同一 event_type 的任务并行执行。使用 Celery 的路由和队列配置来管理任务的并发性，并确保任务在队列中等待。
6. 任务状态管理
任务状态跟踪：使用 Celery 的任务状态管理功能来跟踪每个任务的状态。确保任务仅在其依赖项成功完成后才执行。
7. 工作流和任务状态可视化
状态监控系统：使用 Celery 的结果后端来跟踪任务状态。实现额外的日志记录或监控仪表板，以提供工作流执行的可视化。

# 实现步骤：
## 定义 Event 类：
创建一个包含 trace_id、event_type 和其他必要上下文的 Event 类。
## 配置 Celery：
设置 Celery 的 broker 和 backend。定义任务队列和路由以管理任务并行性。
## 创建任务：
定义接收 Event 对象的 Celery 任务。使用 trace_id 管理任务依赖和状态。
## 定义工作流：
使用配置文件或数据库定义工作流为 DAG。实现解析这些配置并相应触发任务的逻辑。
## 实现 API：
创建一个 API 端点以启动工作流。该端点应创建一个初始 Event 并触发工作流中的第一个任务。
## 监控任务和工作流状态：
使用 Celery 的结果后端跟踪任务状态。实现额外的日志记录或监控仪表板以提供可视化。

# Event结构体
{
    "event_id": str(uuid.uuid4()),
    "trace_id": trace_id,
    "event_type": event_type,
    "task_name": task_name,
    "payload": {}, # 任务输入
    "result": {}, # 任务输出
    "context": {}, # 上下文
    "status": "PENDING", # 任务状态
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
}
## trace_id 
- 同一工作流实例中各个任务执行时的追踪标识

## 


# TODO
## celeryconfig.task_routes

## celeryconfig.task_queues

## 如何通过API提交任务

## 如何通过API出发工作流

## 任务签名（Signatures）

## Worker 守护进程

## 后端监控Flower

## routing_key
- routing_key 是消息从生产者到消费者路径上的“地址标签”，它决定了任务消息经由哪个交换机（Exchange）被转发到哪些队列（Queue）。


# 一些关键概念
## 任务（Task）
- Celery 中定义的可执行函数，如 send_email、generate_report。
- 当你调用 task.delay() 或 task.apply_async() 时，就向 Broker 提交了一条“任务消息”。
- 任务的生命周期。理解任务的生命周期是掌握Celery的关键：
  - PENDING：任务等待被执行
  - STARTED：任务已被worker接收，正在执行
  - SUCCESS：任务执行成功
  - FAILURE：任务执行失败
  - RETRY：任务将被重试
  - REVOKED：任务被撤销

## Worker
- Worker是执行任务的进程，它们监听指定队列，获取并执行任务

## Broker（消息代理）
- Broker负责在客户端和worker之间传递消息。当任务被调用时，它被添加到broker中，然后broker将其分发给可用的worker。

## Backend（结果后端）
- Backend用于存储任务执行结果，使客户端可以检查任务状态和获取返回值。

## 交换机（Exchange）
- 接收生产者（Producer）发出的消息，根据路由规则转发到 0 个、1 个或多个队列。
- 常见类型：
  - direct（直连）——按 routing_key 精确匹配。
  - fanout（广播）——不看 routing_key，把消息推送给所有绑定队列。
  - topic（主题）——可以用 *.news、#. 等通配符匹配多个 routing_key。

## 队列（Queue）
- 临时存储消息的缓冲区。
- Worker 从队列里拉取消息并执行对应的 Task。
- 可以配置队列的优先级、消息过期、持久化等属性。

## 路由（Routing）
- 决定“哪个 Task 消息 应该发往哪个交换机、哪个 routing_key、最终进哪个队列”。
- Celery 中通过 task_routes 或者在 apply_async 时显式指定 exchange、routing_key 实现。


# Worker 实例
# 源商品接收上报并写入缓存，5个进程
celery -A myapp worker --loglevel=info -Q product_src_queue -c 5

# 基于LLM的API生成商品Listing，5个进程
celery -A myapp worker --loglevel=info -Q product_listing_queue -c 5

# 基于ComfyUI服务生成商品图片并存储到OSS服务，2个进程
celery -A myapp worker --loglevel=info -Q product_image_queue -c 2

# 上传商品图片到alibaba图片库，1个进程
celery -A myapp worker --loglevel=info -Q product_upload_queue_ali -c 2

# 发布商品信息到alibaba草稿箱，1个进程
celery -A myapp worker --loglevel=info -Q product_public_queue_ali -c 2

# 上传商品图片到1688相册，1个进程
celery -A myapp worker --loglevel=info -Q product_upload_queue_1688 -c 2

# 发布商品信息到1688商铺，1个进程
celery -A myapp worker --loglevel=info -Q product_public_queue_1688 -c 2
