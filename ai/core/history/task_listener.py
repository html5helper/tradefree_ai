from celery.signals import task_prerun, task_postrun, task_failure, task_retry, task_revoked, task_sent
from ai.dao.entity.task_event import TaskEvent
from ai.dao.entity.product_publish_history import ProductPublishHistory

from datetime import datetime
import json
from ai.service.task_event_service import TaskEventService
from ai.service.product_publish_service import ProductPublishService
from ai.service.actionflow_service import ActionFlowService

task_event_service = TaskEventService()
product_publish_service = ProductPublishService()
actionflow_service = ActionFlowService()

def parse_params(event):
    """解析任务参数"""
    params = {
        'src_platform': event.get('reference_product_platform',''),
        'src_product': event.get('reference_product',event.get('prodid','')),
        'dest_shop': event.get('dest_shop',''),
        'dest_product': event.get('dest_product',''),
        'workflow_name': event.get('workflow','')
    }
    return params

def parse_task_event(task_id: str, task_name: str, event: dict,task_input: dict,task_kwargs: dict) -> TaskEvent:
    """解析任务事件"""
    try:
        trace_id = event.get('trace_id')
        workflow_name = event.get('workflow')
        employee = event.get('employee','system')
        # 取task_type = 从前往后的第三部分
        task_type = task_name.split('.')[2]
        
        # 安全地提取 dest_platform
        if workflow_name and '_' in workflow_name:
            parts = workflow_name.split('_')
            dest_platform = parts[2] if len(parts) > 2 else '--'
        else:
            dest_platform = '--'
        
        # params
        task_params = parse_params(event)
        
        task_event = TaskEvent(
            task_id=task_id,
            task_name=task_name,
            task_owner=employee,
            task_type=task_type,
            task_input=task_input if task_input else None,
            task_kwargs=task_kwargs if task_kwargs else None,
            task_params=json.dumps(task_params),
            task_status='PENDING',
            trace_id=trace_id,
            workflow_name=workflow_name,
            dest_platform=dest_platform,
            created_at=datetime.utcnow()
        )
        return task_event
    except Exception as e:
        print(f"Error parsing task event: {e}")
        return None
    
def parse_product_info(event_data: dict) -> dict:
    """从数据解析产品信息
    {
        trace_id:"",
        product_type:"",
        action_flow_id:"",

        title:"",
        shot_description:"",
        product_name:"",
        video_url:"",
        img_url:"",
        tags:"",
        reference_product:"",
        reference_product_platform:"",
        moq:"",
        price:"",
        delivery_time:"",
        
        shop_name:"",
    }
    Args:
        event_data: 事件数据

    Returns:
        product_info: 产品信息
    """
    try:
        product_info = {
            'trace_id': event_data.get('trace_id', None),
            'action_flow_id': event_data.get('action_flow_id', None),
            'product_type': event_data.get('product_type', None),
            # product info
            'title': event_data.get('title', None),
            'shot_description': event_data.get('shot_description', None),
            'product_name': event_data.get('product_name', None),
            'tags': event_data.get('tags', None),
            'reference_product': event_data.get('reference_product', None),
            'reference_product_platform': event_data.get('reference_product_platform', None),
            'moq': event_data.get('moq', None),
            'price': event_data.get('price', None),
            'delivery_time': event_data.get('delivery_time', None),
            
            # images
            'img_url': event_data.get('video_src_urls', None),
            # video
            'video_url': event_data.get('video_url', None),
            # shop info
            'shop_name': event_data.get('shop_name', None)
        }
        return product_info
    except Exception as e:
        print(f"Error parsing product info: {e}")
        return None

def parse_product_publish_history_from_data(task_event_data: dict, employee_info: dict, product_info: dict) -> ProductPublishHistory:
    """从数据解析发品历史（避免 Session 绑定问题）"""
    try:
        employee_id = employee_info.get("employee_id", None)
        employee_name = employee_info.get("employee_name", None)
        product_publish_history = ProductPublishHistory(
            employee_id=employee_id,
            employee_name=employee_name,
            dest_platform=task_event_data.get('dest_platform', '--'),
            product_type=task_event_data.get('product_type', '--'),
            shop_name=task_event_data.get('shop_name', '--'),
            status='GENERATING',
            trace_id=task_event_data.get('trace_id'),
            last_task_id=task_event_data.get('task_id'),
            last_task_type=task_event_data.get('task_type'),
            last_task_name=task_event_data.get('task_name'),
            last_task_status=task_event_data.get('task_status'),
            product=json.dumps(product_info) if product_info else None,
            action_flow_id=task_event_data.get('action_flow_id', None),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return product_publish_history
    except Exception as e:
        print(f"Error parsing product publish history: {e}")
        return None

@task_sent.connect
def on_task_sent(sender=None, task_id=None, args=None, kwargs=None, **other):
    """任务创建时的初始状态"""
    try:
        event = args[0] if args and isinstance(args[0], dict) else {}
        employee_info = event.get("employee_info",{})
        shop_name = event.get("shop_name", None)
        product_type = event.get("product_type", None)
        
        # 记录任务事件
        task_event = parse_task_event(task_id, sender, event, args, kwargs)
        if task_event is not None:
            # 在添加到数据库前，先提取需要的数据
            task_event_data = {
                'dest_platform': task_event.dest_platform,
                'trace_id': task_event.trace_id,
                'task_id': task_event.task_id,
                'task_type': task_event.task_type,
                'task_name': task_event.task_name,
                'task_status': task_event.task_status,
                'shop_name': shop_name,
                'product_type': product_type
            }
            
            # 添加到数据库
            task_event_service.add(task_event)

            # 只在第一个任务时创建发品历史记录
            # 其他情况，更新记录
            product_publish_history = parse_product_publish_history_from_data(task_event_data, employee_info, {})
            if product_publish_history is not None:
                product_publish_service.save(product_publish_history)

    except Exception as e:
        print(f"Error recording task sent: {e}")

@task_prerun.connect
def before_task_run(sender=None, task_id=None, task=None, args=None, kwargs=None, **other):
    """任务开始执行时的状态"""
    try:
        print(f"[DEBUG] before_task_run called for task_id: {task_id}")
        
        # 先获取任务事件，在 Session 关闭前提取需要的数据
        task_event = task_event_service.get(task_id)
        if task_event is not None:
            # 在 Session 关闭前提取 trace_id
            trace_id = task_event.trace_id
            
            # 更新任务事件状态
            update_result = task_event_service.update(task_id, {'task_status': 'STARTED'})
            
            changes = {
                'last_task_status': 'STARTED',
                'updated_at': datetime.utcnow()
            }
            product_update_result = product_publish_service.update(trace_id, changes)
    except Exception as e:
        print(f"Error recording task prerun: {e}")


@task_postrun.connect
def after_task_run(sender=None, task_id=None,args=None, retval=None, **other):
    try:
        event = args[0] if args and isinstance(args[0], dict) else {}
        task_params = parse_params(retval) 
        
        # 先获取任务事件，在 Session 关闭前提取需要的数据
        task_event = task_event_service.get(task_id)
        if task_event is not None:
            # 在 Session 关闭前提取需要的数据
            trace_id = task_event.trace_id
            task_type = task_event.task_type
            product_status = 'GENERATING'
            
            if task_type == 'storage':
                product_info = parse_product_info(event)
                product_status = 'READY'
            else:
                product_info = {}

            # 更新任务事件状态
            task_event_service.update(task_id, {
                'task_status': 'SUCCESS', 
                'task_params': json.dumps(task_params), 
                'task_output': json.dumps(retval), 
                'finished_at': datetime.utcnow()
            })
            
            action_flow_id = event.get('action_flow_id', None)

            changes = {
                'product': json.dumps(product_info) if product_info else None,
                'action_flow_id': action_flow_id,
                'status': product_status,
                'last_task_status': 'SUCCESS',
                'updated_at': datetime.utcnow()
            }
            product_publish_service.update(trace_id, changes)
    except Exception as e:
        print(f"Error recording task postrun: {e}")

@task_failure.connect
def on_task_failure(sender=None, task_id=None, **other):
    try:
        # 先获取任务事件，在 Session 关闭前提取需要的数据
        task_event = task_event_service.get(task_id)
        if task_event is not None:
            # 在 Session 关闭前提取 trace_id
            trace_id = task_event.trace_id
            
            # 更新任务事件状态
            task_event_service.update(task_id, {'task_status': 'FAILURE', 'finished_at': datetime.utcnow()})
            
            changes = {
                'last_task_status': 'FAILURE',
                'updated_at': datetime.utcnow()
            }
            product_publish_service.update(trace_id, changes)
    except Exception as e:
        print(f"Error recording task failure: {e}")

@task_retry.connect
def on_task_retry(sender=None, task_id=None, **other):
    try:
        # 先获取任务事件，在 Session 关闭前提取需要的数据
        task_event = task_event_service.get(task_id)
        if task_event is not None:
            # 在 Session 关闭前提取 trace_id
            trace_id = task_event.trace_id
            
            # 更新任务事件状态
            task_event_service.update(task_id, {'task_status': 'RETRY', 'finished_at': datetime.utcnow()})
            
            changes = {
                'last_task_status': 'RETRY',
                'updated_at': datetime.utcnow()
            }
            product_publish_service.update(trace_id, changes)
    except Exception as e:
        print(f"Error recording task retry: {e}")

@task_revoked.connect
def on_task_revoked(sender=None, task_id=None, **other):
    try:
        # 先获取任务事件，在 Session 关闭前提取需要的数据
        task_event = task_event_service.get(task_id)
        if task_event is not None:
            # 在 Session 关闭前提取 trace_id
            trace_id = task_event.trace_id
            
            # 更新任务事件状态
            task_event_service.update(task_id, {'task_status': 'REVOKED', 'finished_at': datetime.utcnow()})
            
            changes = {
                'last_task_status': 'REVOKED',
                'updated_at': datetime.utcnow()
            }
            product_publish_service.update(trace_id, changes)
    except Exception as e:
        print(f"Error recording task revoked: {e}")
