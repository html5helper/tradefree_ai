from fastapi import FastAPI, Request
from ai.core.celery_app import app as celery_app
from celery import chain
from ai.core.event import Event
import uuid

api = FastAPI()

@api.post("/workflow/run/amz_to_ali")
async def run_amz_to_ali_workflow(request: Request):
    event = await request.json()
    workflow = chain(
        celery_app.signature('ai.business.resource.tasks.amz_to_ali_src', args=(event,)),
        celery_app.signature('ai.business.listing.tasks.amz_to_ali_listing'),
        celery_app.signature('ai.business.image.tasks.amz_to_ali_image'),
        celery_app.signature('ai.business.upload_img.tasks.amz_to_ali_upload'),
        celery_app.signature('ai.business.public.tasks.amz_to_ali_public'),
    )
    result = workflow.apply_async()
    return {"trace_id": result.id}

@api.post("/workflow/run/amz_to_1688")
async def run_amz_to_1688_workflow(request: Request):
    event = await request.json()
    workflow = chain(
        celery_app.signature('ai.business.resource.tasks.amz_to_1688_src', args=(event,)),
        celery_app.signature('ai.business.listing.tasks.amz_to_1688_listing'),
        celery_app.signature('ai.business.image.tasks.amz_to_1688_image'),
        celery_app.signature('ai.business.upload_img.tasks.amz_to_1688_upload'),
        celery_app.signature('ai.business.public.tasks.amz_to_1688_public'),
    )
    result = workflow.apply_async()
    return {"trace_id": result.id}

@api.post("/workflow/run/1688_to_1688")
async def run_1688_to_1688_workflow(request: Request):
    event = await request.json()
    workflow = chain(
        celery_app.signature('ai.business.resource.tasks._1688_to_1688_src', args=(event,)),
        celery_app.signature('ai.business.listing.tasks._1688_to_1688_listing'),
        celery_app.signature('ai.business.image.tasks._1688_to_1688_image'),
        celery_app.signature('ai.business.upload_img.tasks._1688_to_1688_upload'),
        celery_app.signature('ai.business.public.tasks._1688_to_1688_public'),
    )
    result = workflow.apply_async()
    return {"trace_id": result.id}

@api.post("/workflow/run/ali_to_ali")
async def run_ali_to_ali_workflow(request: Request):
    event = await request.json()
    workflow = chain(
        celery_app.signature('ai.business.resource.tasks.ali_to_ali_src', args=(event,)),
        celery_app.signature('ai.business.listing.tasks.ali_to_ali_listing'),
        celery_app.signature('ai.business.image.tasks.ali_to_ali_image'),
        celery_app.signature('ai.business.upload_img.tasks.ali_to_ali_upload'),
        celery_app.signature('ai.business.public.tasks.ali_to_ali_public'),
    )
    result = workflow.apply_async()
    return {"trace_id": result.id} 

@api.post("/workflow/run/social_to_ali")
async def run_social_to_ali_workflow(request: Request):
    event = await request.json()
   
    res = celery_app.send_task('ai.business.social2product.tasks.fetch_social_total', args=[event])
    return {"trace_id": res.id}