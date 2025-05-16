from ai.core.celery_app import app
from ai.business.service.dify_service import DifyService

service = DifyService()

@app.task
def amz_to_ali_src(event_dict: dict):
    return service.apply(event_dict['data'])

@app.task
def amz_to_1688_src(event_dict: dict):
    return service.apply(event_dict['data'])

@app.task
def _1688_to_1688_src(event_dict: dict):
    return service.apply(event_dict['data'])

@app.task
def ali_to_ali_src(event_dict: dict):
    return service.apply(event_dict['data'])

@app.task
def social_to_ali_src(event_dict: dict):
    return service.apply(event_dict['data'])