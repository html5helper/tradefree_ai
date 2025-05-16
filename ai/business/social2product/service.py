from ai.business.dify_client import DifyClient
import json
import datetime

class DifySocial2ProductService:
    def __init__(self):
        self.client = DifyClient()

    def social_record_total_count(self,payload:dict) -> dict:
        """Run a task to get the social record total count."""
        # Send the request
        response = self.client.post( "b811f832-47e7-4a92-8aff-82a6859be328", "app-GvSm89L42OluDU2JFyaDOCvM",  payload)
        # Handle the response
        output = response["data"]["outputs"]
        return output
    
    def social_to_ali_src(self,payload:dict) -> dict:
        """Run a task to get the social to ali src."""
        # Send the request
        response = self.client.post( "c25c3f82-61d0-44f0-bc5a-d0bff52f8aa2", "app-23SX7AOxwVCZvaXvtupFDsaT", payload)
        # Handle the response 
        output = response["data"]["outputs"]
        return output
    
    def social_to_ali_listing(self,payload:dict) -> dict:
        """Run a task to get the social to ali listing."""
        response = self.client.post( "71012911-41b9-4d66-9c19-d666f2389d7e", "app-JMJ87fMuTgYtOPlRGJNk5DVH", payload)
        # Handle the response   
        output = response["data"]["outputs"]
        return output

    def social_to_ali_image(self,payload:dict) -> dict:
        """Run a task to get the social to ali image."""
        response = self.client.post( "41635577-659f-4d56-ae1d-a67131c94185", "app-CrxTvw9sMXREZohs8jVqsEs3", payload)
        # Handle the response
        output = response["data"]["outputs"]
        return output
    
    def social_to_ali_upload(self,payload:dict) -> dict:
        """Run a task to get the social to ali upload."""
        run_workflow = "71012911-41b9-4d66-9c19-d666f2389d7e"
        api_key = "app-JMJ87fMuTgYtOPlRGJNk5DVH"

        # Send the request
        response = self.client.post( run_workflow, api_key, payload)

        # Handle the response
        items = response["data"]["outputs"]["items"]
        return items
    
    def social_to_ali_public(self,payload:dict) -> dict:
        """Run a task to get the social to ali public."""
        run_workflow = "71012911-41b9-4d66-9c19-d666f2389d7e"
        api_key = "app-JMJ87fMuTgYtOPlRGJNk5DVH"

        # Send the request
        response = self.client.post( run_workflow, api_key, payload)

        # Handle the response
        items = response["data"]["outputs"]["items"]
        return items
        
        
