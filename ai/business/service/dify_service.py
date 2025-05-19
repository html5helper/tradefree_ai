from ai.business.dify_client import DifyClient
from ai.core.data_event import DataEvent
from celery import current_task
from ai.config.celeryconfig import DIFY_CONFIG
import json

class DifyService:
    def __init__(self):
        self.client = DifyClient()

    # 合并两个dict，如果key相同，则新的value覆盖旧的value
    def merge_dict(self,dict1:dict,dict2:dict) -> dict:
        return {**dict1, **dict2}

    def apply(self, input: dict) -> dict:
        output = input.copy()
        
        task_id = current_task.request.id
        output['task_id'] = task_id
        # output['task_name'] = current_task.name
        
        return output
    
    def run_task(self,task_name:str,payload:dict) -> dict:
        """Run a dify task and return the output."""
        payload['task_id'] = current_task.request.id
        # 将paylaod中的所有字段都转化为字符串类型，包括dict,list,tuple,set
        # for key, value in payload.items():
        #     if isinstance(value, dict):
        #         payload[key] = json.dumps(value)
        #     elif isinstance(value, list):
        #         payload[key] = json.dumps(value)
        #     elif isinstance(value, tuple):
        #         payload[key] = json.dumps(value)
        #     elif isinstance(value, set):
        #         payload[key] = json.dumps(value)
        #     else:
        #         payload[key] = str(value)
        # print("dify payload=",payload)
        # 从配置中获取 workflow_id 和 api_key

        config = DIFY_CONFIG[task_name]
        # Send the request
        response = self.client.post(
            config['workflow_id'],
            config['api_key'],
            payload
        )
        # Handle the response
        output = response["data"]["outputs"]
        
        # 如果output为None，则抛出异常
        if output is None:
            raise Exception(f"Dify API returned None output for task {task_name}")
        
        return {**payload, **output} 
 