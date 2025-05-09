import requests
import json
import datetime

class DifyClient:
    def __init__(self):
        self.base_url = "http://dify.tradefree.ai/v1"
        self.endpoint = "workflows/run"
        self.client_user = "celery_task"

    def post(self,workflow_id: str, api_key: str,inputs: dict) -> dict:
        """Send a POST request to the specified endpoint with dynamic parameters."""
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            "workflow_id": workflow_id,
            "inputs": inputs,
            "response_mode": "blocking",
            "user": self.client_user
        }
        response = requests.post(f'{self.base_url}/{self.endpoint}', headers=headers, json=payload,timeout=900)
        response.raise_for_status()
        return response.json()

