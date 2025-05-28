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
                
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"\n=== Dify API HTTP Error ===")
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Headers: {dict(e.response.headers)}")
            print(f"Response Body: {e.response.text}")
            print(f"Request Payload: {json.dumps(payload, indent=2)}")
            print(f"Stack Trace: {traceback.format_exc()}")
            print(f"=====================\n")
            raise
        except Exception as e:
            print(f"\n=== Dify API Unexpected Error ===")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {str(e)}")
            print(f"Request Payload: {json.dumps(payload, indent=2)}")
            print(f"Stack Trace: {traceback.format_exc()}")
            print(f"=====================\n")
            raise

