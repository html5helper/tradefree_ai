import time
import logging
from ai.business.example.tasks import task1, task2, task3
from celery import chain, group

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_serial_workflow():
    """测试串行工作流"""
    logger.info("Starting serial workflow test")
    
    # 创建串行工作流
    workflow = chain(
        task1.s({"param1": "value1", "trace_id": "serial_test"}),
        task2.s(),
        task3.s()
    )
    
    # 执行工作流
    result = workflow.apply_async()
    
    logger.info(f"Serial workflow started with task_id: {result.id}")
    
    # 等待结果
    try:
        final_result = result.get(timeout=10)
        logger.info(f"Serial workflow completed with result: {final_result}")
    except Exception as e:
        logger.error(f"Serial workflow failed: {e}")

def test_parallel_workflow():
    """测试并行工作流"""
    logger.info("Starting parallel workflow test")
    
    # 创建并行工作流
    workflow = group(
        task1.s({"param1": "value1", "trace_id": "parallel_test_1"}),
        task2.s({"param2": "value2", "trace_id": "parallel_test_2"}),
        task3.s({"param3": "value3", "trace_id": "parallel_test_3"})
    )
    
    # 执行工作流
    result = workflow.apply_async()
    
    logger.info(f"Parallel workflow started with task_id: {result.id}")
    
    # 等待结果
    try:
        final_result = result.get(timeout=10)
        logger.info(f"Parallel workflow completed with results: {final_result}")
    except Exception as e:
        logger.error(f"Parallel workflow failed: {e}")

def test_custom_trace_id():
    """测试自定义 trace_id"""
    logger.info("Starting custom trace_id test")
    
    custom_trace_id = "custom_test_123"
    
    # 创建工作流
    workflow = chain(
        task1.s({"param1": "value1", "trace_id": custom_trace_id}),
        task2.s(),
        task3.s()
    )
    
    # 执行工作流
    result = workflow.apply_async()
    
    logger.info(f"Custom trace_id workflow started with task_id: {result.id}")
    
    # 等待结果
    try:
        final_result = result.get(timeout=10)
        logger.info(f"Custom trace_id workflow completed with result: {final_result}")
    except Exception as e:
        logger.error(f"Custom trace_id workflow failed: {e}")

if __name__ == "__main__":
    logger.info("Starting workflow tests")
    
    # 运行串行工作流测试
    test_serial_workflow()
    
    # 等待一段时间，确保日志清晰
    time.sleep(2)
    
    # 运行并行工作流测试
    test_parallel_workflow()
    
    # 等待一段时间，确保日志清晰
    time.sleep(2)
    
    # 运行自定义 trace_id 测试
    test_custom_trace_id()
    
    logger.info("All workflow tests completed")