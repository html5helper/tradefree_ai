import requests
import json
import traceback

class DifyClient:
    def __init__(self,base_url:str):
        self.base_url = base_url
        self.endpoint = "workflows/run"
        self.client_user = "celery_task"

    def post(self, workflow_id: str, api_key: str, inputs: dict) -> dict:
        """Send a POST request to the specified endpoint with dynamic parameters."""
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            "workflow_id": workflow_id,
            "inputs": {"data": json.dumps(inputs)},
            "response_mode": "blocking",
            "user": self.client_user
        }
        
        try:
            print(f"\n=== Dify API Request ===")
            print(f"URL: {self.base_url}/{self.endpoint}")
            print(f"Headers: {json.dumps(headers, indent=2)}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            print(f"=====================\n")
            
            response = requests.post(
                f'{self.base_url}/{self.endpoint}',
                headers=headers,
                json=payload,
                timeout=900
            )
            
            if response.status_code != 200:
                print(f"\n=== Dify API Error ===")
                print(f"Status Code: {response.status_code}")
                print(f"Response Headers: {dict(response.headers)}")
                print(f"Response Body: {response.text}")
                print(f"Request Payload: {json.dumps(payload, indent=2)}")
                print(f"=====================\n")
                response.raise_for_status()
            
            response_data = response.json()
            
            # 检查响应格式
            if not isinstance(response_data, dict):
                raise ValueError(f"Invalid response format: {response_data}")
            
            if 'data' not in response_data:
                raise ValueError(f"Missing 'data' in response: {response_data}")
            
            if 'outputs' not in response_data['data']:
                raise ValueError(f"Missing 'outputs' in response data: {response_data['data']}")
            
            return response_data
            
        except Exception as e:
            print(f"\n=== Dify API Exception ===")
            print(f"Error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            print(f"=====================\n")
            raise

