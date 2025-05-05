import requests
import json
import datetime

class DifyClient:
    def __init__(self):
        self.base_url = "http://dify.html5core.com/v1"
        self.endpoint = "workflows/run"

    def post(self,workflow_id: str, api_key: str, user: str,inputs: dict) -> dict:
        """Send a POST request to the specified endpoint with dynamic parameters."""
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            "workflow_id": workflow_id,
            "inputs": inputs,
            "response_mode": "blocking",
            "user": user
        }
        response = requests.post(f'{self.base_url}/{self.endpoint}', headers=headers, json=payload,timeout=900)
        response.raise_for_status()
        return response.json()

