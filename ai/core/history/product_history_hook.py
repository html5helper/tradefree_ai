from ai.dao.entity.product_history import ProductHistory
from ai.service.product_history_service import ProductHistoryService
from datetime import datetime
import json

product_history_service = ProductHistoryService()

class ProductHistoryHook:
    """发品历史钩子
    Args:
        task_event_data: 任务事件数据
        employee_info: 员工信息
        product_info: 产品信息

    Returns:
        ProductHistory: 发品历史
    """
    """ 发品历史状态说明：
        - PENDING: 任务已创建，等待执行
        - STARTED: 任务已开始执行
        - SUCCESS: 任务执行成功，发品成功
        - FAILURE: 任务执行失败，发品失败
    """
    def __init__(self):
        pass

    def pending(self, task_event: dict, task_input: dict) -> dict:
        """任务事件待执行状态"""
        task_type = task_event.get('task_type', None)
        trace_id = task_event.get('trace_id', None)
        process = self.get_product_process_type(task_type,'pending')
        process_type = process.get('process_type', None)
        changes = process.get('changes', None)

        if(process_type == 'collect'):
            if(task_type == 'resource'):
                return self.save_product_history(task_event, task_input)
            else:
                product_info = self.parse_collect_product_info(task_input)
                data = self.parse_update_task_info({**changes, **{'collect_product': json.dumps(product_info)}},task_event)
                return product_history_service.update(trace_id, data)
        elif(process_type == 'generate'):
            product_info = self.parse_collect_product_info(task_input)
            data = self.parse_update_task_info({**changes, **{'generate_product': json.dumps(product_info)}},task_event)
            return product_history_service.update(trace_id, data)
                
        elif(process_type == 'publish'):
            product_info = self.parse_publish_product_info(task_input)
            data = self.parse_update_task_info({**changes, **{'publish_product': json.dumps(product_info)}},task_event)
            return product_history_service.update(trace_id, data)
        
        return None

    def started(self, task_event: dict, task_input: dict) -> dict:
        """任务事件执行中状态"""
        task_type = task_event.get('task_type', None)
        trace_id = task_event.get('trace_id', None)
        process = self.get_product_process_type(task_type,'started')
        process_type = process.get('process_type', None)
        changes = process.get('changes', None)
        data = self.parse_update_task_info({**changes},task_event)
        return product_history_service.update(trace_id, data)

    def success(self, task_event: dict, task_input: dict,task_output: dict) -> ProductHistory:
        """任务事件执行成功状态"""
        task_type = task_event.get('task_type', None)
        trace_id = task_event.get('trace_id', None)
        process = self.get_product_process_type(task_type,'success')
        process_type = process.get('process_type', None)
        changes = process.get('changes', None)

        data = {}
        if(process_type == 'collect'):
            collect_product = self.parse_collect_product_info(task_input)
            data = self.parse_update_task_info({**changes, **{'collect_product': json.dumps(collect_product)}},task_event)
        elif(process_type == 'generate'):
            generate_product = self.parse_generate_product_info(task_output)
            if(changes.get('publish_status') == 'PENDING' and changes.get('generate_status') == 'SUCCESS'):
                publish_product = json.dumps(task_output)
            else:
                publish_product = None
            data = self.parse_update_task_info({**changes, **{'generate_product': json.dumps(generate_product),'publish_product': publish_product}},task_event)
        elif(process_type == 'publish'):
            publish_product = self.parse_publish_product_info(task_output)
            data = self.parse_update_task_info({**changes, **{'publish_product': json.dumps(publish_product)}},task_event)
        
        return product_history_service.update(trace_id, data)
    
    def failure(self, task_event: dict) -> ProductHistory:
        """任务事件执行失败状态"""
        task_type = task_event.get('task_type', None)
        trace_id = task_event.get('trace_id', None)
        process = self.get_product_process_type(task_type,'failure')
        process_type = process.get('process_type', None)
        changes = process.get('changes', None)
        
        data = self.parse_update_task_info(changes,task_event)
        return product_history_service.update(trace_id, data)
    
    def parse_update_task_info(self,base_data: dict, task_event: dict) -> dict:
        """从任务事件解析任务信息"""
        data = {
            'last_task_id': task_event.get('task_id', None),
            'last_task_type': task_event.get('task_type', None),
            'last_task_name': task_event.get('task_name', None),
            'last_task_status': task_event.get('task_status', None)
        }
        return {**base_data, **data}

    def parse_collect_product_info(self,task_input: dict) -> dict:
        """从数据解析产品信息"""
        product_info = task_input.copy()
        product_info.pop('access', None)
        return product_info
    
    def parse_generate_product_info(self,task_input: dict) -> dict:
        """从数据解析产品信息"""
        product_info = task_input.copy()
        return product_info
        # result = {
        #     'trace_id': task_input.get('trace_id', None),
        #     'template_id': task_input.get('template_id', None),
        #     'product_type': task_input.get('product_type', None),
        #     # product info
        #     'title': task_input.get('title', None),
        #     'shot_description': task_input.get('shot_description', None),
        #     'product_name': task_input.get('product_name', None),
        #     'tags': task_input.get('tags', None),
        #     'reference_product': task_input.get('reference_product', None),
        #     'reference_product_platform': task_input.get('reference_product_platform', None),
        #     'moq': task_input.get('moq', None),
        #     'price': task_input.get('price', None),
        #     'delivery_time': task_input.get('delivery_time', None),
            
        #     # images
        #     'img_url': task_input.get('video_src_urls', None),
        #     # video
        #     'video_url': task_input.get('video_url', None),
        #     # shop info
        #     'shop_name': task_input.get('shop_name', None)
        # }
        # return result

    def parse_publish_product_info(self,task_input: dict) -> dict:
        """从数据解析产品信息"""
        try:
            product_info = task_input.copy()
            if(product_info.get('video_src_urls')):
                product_info['img_url'] = product_info.get('video_src_urls', None)
            return product_info
            # result = {
            #     'trace_id': product_info.get('trace_id', None),
            #     'template_id': product_info.get('template_id', None),
            #     'product_type': product_info.get('product_type', None),
            #     # product info
            #     'title': product_info.get('title', None),
            #     'shot_description': product_info.get('shot_description', None),
            #     'product_name': product_info.get('product_name', None),
            #     'tags': product_info.get('tags', None),
            #     'reference_product': product_info.get('reference_product', None),
            #     'reference_product_platform': product_info.get('reference_product_platform', None),
            #     'moq': product_info.get('moq', None),
            #     'price': product_info.get('price', None),
            #     'delivery_time': product_info.get('delivery_time', None),
                
            #     # images
            #     'img_url': product_info.get('video_src_urls', None),
            #     # video
            #     'video_url': product_info.get('video_url', None),
            #     # shop info
            #     'shop_name': product_info.get('shop_name', None)
            # }
            # return result
        except Exception as e:
            print(f"Error parsing product info: {e}")
            return None
        
    def get_product_process_type(self, task_type: str,status_type: str) -> str:
        """获取产品处理类型
        Args:
            task_event: 任务事件

        Returns:
            product_process_type: 产品处理类型
        """
        process_type = None
        changes = {}
        if(task_type in ['resource']):
            process_type = 'collect'
            if(status_type == 'pending'):
                changes = {'collect_status': 'PENDING'}
            elif(status_type == 'started'):
                changes = {'collect_status': 'STARTED'}
            elif(status_type == 'success'):
                changes = {'collect_status': 'SUCCESS','generate_status': 'PENDING'}
            elif(status_type == 'failure'):
                changes = {'collect_status': 'FAILURE'}
        elif(task_type in ['listing', 'maskword','image', 'video','storage']):
            process_type = 'generate'
            if(status_type == 'failure'):
                changes = {'generate_status': 'FAILURE'}
            elif(task_type == 'listing' and status_type == 'pending'):
                changes = {'generate_status': 'PENDING'}
            elif(task_type == 'storage' and status_type == 'success'):
                changes = {'generate_status': 'SUCCESS','publish_status': 'PENDING'}
            else:
                changes = {'generate_status': 'STARTED'}
        elif(task_type in ['upload_img','upload_video','public']):
            process_type = 'publish'
            if(status_type == 'failure'):
                changes = {'publish_status': 'FAILURE'}
            elif(task_type == 'upload_img' and status_type == 'pending'):
                changes = {'publish_status': 'PENDING'}
            elif(task_type == 'public' and status_type == 'success'):
                changes = {'publish_status': 'SUCCESS'}
            else:
                changes = {'publish_status': 'STARTED'}
        
        
        return {'process_type':process_type,'changes':changes}
        
    def save_product_history(self,task_event: dict, task_input: dict) -> ProductHistory:
        """从数据解析发品历史（避免 Session 绑定问题）"""
        try:
            access = task_input.get('access',{})
            workflow = task_event.get('workflow_name', None)
            src_platform = workflow.split('_')[0]
            dest_platform = workflow.split('_')[2]

            product_info = self.parse_collect_product_info(task_input)

            product_history = ProductHistory(
                trace_id=task_event.get('trace_id'),
                employee_id=access.get("employee_id", None),
                employee_name=access.get("employee_name", None),
                product_type=access.get('product_type', '--'),
                collect_status='PENDING',
                collect_product=json.dumps(product_info),
                generate_status=None,
                generate_product=None,
                publish_status=None,
                publish_product=None,
                src_platform=src_platform,
                dest_platform=dest_platform,
                dest_shop_name=access.get('shop_name', '--'),
                last_task_id=task_event.get('task_id'),
                last_task_type=task_event.get('task_type'),
                last_task_name=task_event.get('task_name'),
                last_task_status=task_event.get('task_status'),
                template_id=access.get('template_id', None),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            product_history_service.save_or_update(product_history)

            return product_history
        except Exception as e:
            print(f"Error parsing product publish history: {e}")
            return None
    