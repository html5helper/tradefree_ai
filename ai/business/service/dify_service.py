from ai.business.dify_client import DifyClient
from ai.core.data_event import DataEvent
from celery import current_task
from ai.config.celeryconfig import DIFY_CONFIG


class DifyService:
    def __init__(self):
        self.client = DifyClient()

    def apply(self, input: dict) -> dict:
        output = input.copy()
        
        task_id = current_task.request.id
        output['task_id'] = task_id
        # output['task_name'] = current_task.name
        
        return output
    
    def run_task(self,task_name:str,payload:dict) -> dict:
        """Run a dify task and return the output."""
        payload['task_id'] = current_task.request.id
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
        output['trace_id'] = payload['trace_id']
        return output
 