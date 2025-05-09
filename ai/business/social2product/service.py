from ai.business.dify_client import DifyClient
import json
import datetime

class DifySocial2ProductService:
    def __init__(self):
        self.client = DifyClient()


    def social_record_total_count(self,payload:dict) -> dict:
        """Run a task to get the social record total count."""
        run_workflow = "30f83aad-9cc2-446e-80ca-3eeceecb9e0e"
        api_key = "app-ZSF37vjGwUCRzgxql9jl8TG4"
        client_user = "scheduler_task"

        # Log the request
        print("Request payload:", json.dumps(payload))

        # Send the request
        response = self.client.post( run_workflow, api_key, client_user, payload)

        # Handle the response
        print("Response:", response)
        total = response["data"]["outputs"]["total"]
        return total

    def create_products_from_social_page_records(self,payload:dict) -> list:
        """Run a task to create some products from social records using the Dify client."""
        run_workflow = "10484768-e4b4-4b81-9feb-8d83b21474b8"
        api_key = "app-6fiupTWdMHDYjxodwSAmlVxi"
        client_user = "scheduler_task"

        # Log the request
        print("Request payload:", json.dumps(payload))

        # Send the request
        response = self.client.post( run_workflow, api_key, client_user, payload)

        # Handle the response
        print("Response:", response)
        urls = response["data"]["outputs"]["urls"]
        return urls
