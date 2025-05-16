from ai.core.celery_app import app
from ai.business.service.dify_service import DifyService

service = DifyService()


@app.task
def amz_to_ali_listing(data: dict):
    return service.run_task("product_listing",data)

@app.task
def amz_to_1688_listing(data: dict):
    return service.run_task("product_listing",data)

@app.task
def _1688_to_1688_listing(data: dict):
    return service.run_task("product_listing",data)

@app.task
def ali_to_ali_listing(data: dict):
    return service.run_task("product_listing",data)

@app.task
def social_to_ali_listing(data: dict):
    return service.apply(data)