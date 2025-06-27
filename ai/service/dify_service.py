from ai.business.dify_client import DifyClient
from ai.config.celeryconfig import DIFY_CONFIG, DIFY_BASE_URL

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
 