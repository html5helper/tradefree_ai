from celery.signals import task_prerun, task_postrun, task_failure, task_retry, task_revoked, task_sent
from ai.dao.entity.task_event import TaskEvent
from ai.dao.entity.product_publish_history import ProductPublishHistory
from ai.dao.entity.action_flow import ActionFlow

from datetime import datetime
import json
from ai.service.task_event_service import TaskEventService
from ai.service.product_publish_Service import ProductPublishService
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
        "imgs": "/opt/data/img/b6928670-76a7-4067-89eb-2a97d5a4cf3a/1750218411067_3848.png,/opt/data/img/b6928670-76a7-4067-89eb-2a97d5a4cf3a/1750218411776_7752.png,/opt/data/img/b6928670-76a7-4067-89eb-2a97d5a4cf3a/1750218412727_6330.png,/opt/data/img/b6928670-76a7-4067-89eb-2a97d5a4cf3a/1750218413195_5172.png,/opt/data/img/b6928670-76a7-4067-89eb-2a97d5a4cf3a/1750218413656_6588.png",
        "price": "0.15",
        "title": "Nightlight Waterproof PVC Paul Et Shark Stickers Car Decorative Omerta Sticker Shark Sticker 3d",
        "trace_id": "e0c06881-4711-43b0-b6ec-64f252ef8b41",
        "description": "Elevate your car's interior or nightstand with our Nightlight Waterproof PVC Paul Et Shark 3D Sticker, a bold and eye-catching decorative piece that combines pop culture charm with functional lighting. Made from high-quality waterproof PVC material, this sticker is not only durable but also safe to use in humid or wet environments, making it perfect for bathrooms, kitchens, or even outdoor displays. The 3D design of the shark adds depth and dimension, while the embedded LED light offers a soft glow that enhances visibility without being harsh. This sticker features the iconic Paul Et Shark character from the French cartoon series, appealing to fans of the show and lovers of unique car decor. Whether you're looking to add a touch of fun to your dashboard, personalize your phone case, or create a themed nightlight for your child's room, this sticker delivers both style and utility. Its easy-to-apply adhesive ensures a secure fit on smooth surfaces like glass, plastic, or metal, and the waterproof nature of the material makes it resistant to fading or peeling over time. Ideal for car enthusiasts, collectors, and anyone who wants to infuse their space with a sense of adventure and personality.",
        "product_type": "sticker",
        "delivery_time": "7 days",
        "published_shop": "ali_shop2",
        "reference_product": "https://www.alibaba.com/product-detail/Nightlight-Waterproof-PVC-Paul-Et-Shark_1601376877002.html",
        "reference_product_platform": "ali",
        "shot_description": "Waterproof 3D Paul Et Shark Sticker with LED Light - Durable PVC material designed for car decor or nightstands, featuring the iconic cartoon character for fans of the series. Perfect for adding a pop of color and illumination to any surface.",
        "tags": "paul et shark 3d sticker waterproof car decor led nightlight pvc stickers cartoon character stickers car dashboard decoration waterproof vinyl stickers 3d animal stickers kids room decor cartoon stickers for phone cases",
        "product_name": "Nightlight Waterproof PVC Paul Et Shark 3D Sticker",
        "str_photos": "id_4=13990297301,url_4=https://sc04.alicdn.com/kf/H8381568913fa4db99072983fcb156364C/231139578/H8381568913fa4db99072983fcb156364C.png,url_2=https://sc04.alicdn.com/kf/H10c2f84b082941c99324eb49e3bbb93b9/231139578/H10c2f84b082941c99324eb49e3bbb93b9.png,url_3=https://sc04.alicdn.com/kf/Hb17ea35e8de3408ab46ee1fa4cd9945fq/231139578/Hb17ea35e8de3408ab46ee1fa4cd9945fq.png,url_0=https://sc04.alicdn.com/kf/H70b218560e0b46efa167269acaf9a656a/231139578/H70b218560e0b46efa167269acaf9a656a.png,url_1=https://sc04.alicdn.com/kf/Hc1511d0d2c2640ddab0499ef6819b85a3/231139578/Hc1511d0d2c2640ddab0499ef6819b85a3.png,id_1=13994184757,id_0=13990321245,id_3=13985365718,id_2=13985353692",
        "video_url": "http://dify.html5core.com/svg/c61ea5bf-ba4c-4e3e-9564-1c98eb31792d_with_audio.mp4",
        "video_id": "6000302396297"
    }
    Args:
        event_data: 事件数据

    Returns:
        product_info: 产品信息
    """
    try:
        product_info = {
            'trace_id': event_data.get('trace_id', None),
            # product info
            'title': event_data.get('title', None),
            'description': event_data.get('description', None),
            'shot_description': event_data.get('shot_description', None),
            'tags': event_data.get('tags', None),
            'delivery_time': event_data.get('delivery_time', None),
            'price': event_data.get('price', None),
            'product_name': event_data.get('product_name', None),
            # images
            'imgs': event_data.get('imgs', None),
            'str_photos': event_data.get('str_photos', None),
            # video
            'video_url': event_data.get('video_url', None),
            'video_id': event_data.get('video_id', None),
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
            shop_name=task_event_data.get('shop_cn_name', '--'),
            status='PENDING',
            trace_id=task_event_data.get('trace_id'),
            last_task_id=task_event_data.get('task_id'),
            last_task_type=task_event_data.get('task_type'),
            last_task_name=task_event_data.get('task_name'),
            last_task_status=task_event_data.get('task_status'),
            product=json.dumps(product_info) if product_info else None,
            actionflow="{}",
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
        shop_cn_name = event.get("shop_cn_name", None)
        
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
                'shop_cn_name': shop_cn_name
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
            
            # 更新任务事件状态
            task_event_service.update(task_id, {
                'task_status': 'SUCCESS', 
                'task_params': json.dumps(task_params), 
                'task_output': json.dumps(retval), 
                'finished_at': datetime.utcnow()
            })
            
            if task_type == 'storage':
                product_info = parse_product_info(event)
            else:
                product_info = {}

            action_flow_id = event.get('action_flow_id', None)
            action_flow_item = actionflow_service.get(action_flow_id)
            if action_flow_item:
                actionflow = action_flow_item.action_flow if hasattr(action_flow_item, 'action_flow') else ""
            else:
                actionflow = ""

            changes = {
                'product': json.dumps(product_info) if product_info else None,
                'actionflow': actionflow if actionflow else "{}",
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
