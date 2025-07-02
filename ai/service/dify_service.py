from ai.business.dify_client import DifyClient
from ai.config.celeryconfig import DIFY_CONFIG, DIFY_BASE_URL
import json

class DifyService:
    def __init__(self):
        self.client = DifyClient(DIFY_BASE_URL)

    # 合并两个dict，如果key相同，则新的value覆盖旧的value
    def merge_dict(self,dict1:dict,dict2:dict) -> dict:
        return {**dict1, **dict2}

    def apply(self, input: dict) -> dict:
        output = input.copy()
        
        return output
    
    def run_task(self,task_name:str,payload:dict) -> dict:
        """Run a dify task and return the output."""
        input = payload.copy()
        if 'access' in input:
            input.pop('access')

        config = DIFY_CONFIG[task_name]
        # Send the request
        response = self.client.post(
            config['workflow_id'],
            config['api_key'],
            input
        )
        
        # Handle the response
        output = response["data"]["outputs"]

                # 如果output为None，则抛出异常
        if output is None:
            raise Exception(f"Dify API returned None output for task {task_name}")

        if 'code' not in output:
            raise ValueError(f"Missing 'code' in response outputs: {output}")
            
        if output['code'] != 200:
            raise ValueError(f"Task execution failed with code {output['code']}: {output}")
        
        return {**payload, **output} 
    
    # img_inpaint
    def image_inpaint(self,payload:dict) -> dict:
        """Run img_inpaint task with flat input parameters (not wrapped in data field)"""
        input = payload.copy()
        if 'access' in input:
            input.pop('access')

        config = DIFY_CONFIG['img_inpaint']
        
        # 为 img_inpaint 工作流创建特殊的请求格式（扁平参数）
        headers = {
            'Authorization': f'Bearer {config["api_key"]}',
            'Content-Type': 'application/json'
        }
        payload_special = {
            "workflow_id": config['workflow_id'],
            "inputs": input,  # 直接传递输入，不包装在 data 字段中
            "response_mode": "blocking",
            "user": "celery_task"
        }
        
        try:

            import requests
            response = requests.post(
                f'{DIFY_BASE_URL}/workflows/run',
                headers=headers,
                json=payload_special,
                timeout=900
            )
            
            if response.status_code != 200:
                response.raise_for_status()
            
            response_data = response.json()
            
            # 检查响应格式（参考 run_task 的处理方式）
            if not isinstance(response_data, dict):
                raise ValueError(f"Invalid response format: {response_data}")
            
            if 'data' not in response_data:
                raise ValueError(f"Missing 'data' in response: {response_data}")
            
            if 'outputs' not in response_data['data']:
                raise ValueError(f"Missing 'outputs' in response data: {response_data['data']}")
            
            output = response_data["data"]["outputs"]
            
            # 如果output为None，则抛出异常
            if output is None:
                raise Exception(f"Dify API returned None output for img_inpaint")

            if 'code' not in output:
                raise ValueError(f"Missing 'code' in response outputs: {output}")
                
            if output['code'] != 200:
                raise ValueError(f"Task execution failed with code {output['code']}: {output}")
            
            return {**payload, **output}
            
        except Exception as e:
            print(f"\n=== Dify API Exception (img_inpaint) ===")
            print(f"Error: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            print(f"=====================\n")
            raise
 