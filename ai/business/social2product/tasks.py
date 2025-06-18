from ai.core.celery_app import app
from celery import chain, chord
from ai.business.social2product.service import DifySocial2ProductService
import uuid

@app.task
def fetch_social_total(event_in:dict):
    """
    获取总记录数并设定分页大小
    """
    trace_id = str(uuid.uuid4())

    # event 为上述 Event JSON
    platform = event_in["context"]["platform"] 
    
    print(f"fetch_social_total,event_in: {event_in}")

    # 假设获取总记录数的逻辑
    service = DifySocial2ProductService()
    payload = {
        "trace_id": trace_id,
        "platform": platform
    }
    total = service.social_record_total_count(payload)

    page_size = 30
    pages = (total + page_size - 1) // page_size
    event_in['result'] = {'total': total, 'page_size': page_size, 'pages': pages}

    # 分页异步触发 chain
    for page in range(1, pages + 1):
        event_with_page = event_in.copy()
        event_with_page['trace_id'] = str(uuid.uuid4())
        event_with_page['context']['page'] = page
        event_with_page['context']['page_size'] = page_size
        app.send_task('ai.business.resource.tasks.social_to_ali_src', args=[event_with_page])
        workflow = chain(
            app.signature('ai.business.resource.tasks.social_to_ali_src', args=(event_with_page,)),
            app.signature('ai.business.listing.tasks.social_to_ali_listing'),
        #     app.signature('ai.business.image.tasks.social_to_ali_image'),
        #     app.signature('ai.business.upload_img.tasks.social_to_ali_upload'),
        #     app.signature('ai.business.public.tasks.social_to_ali_public'),
         )
        workflow.apply_async()
    return {"status": "dispatched", "pages": pages}
