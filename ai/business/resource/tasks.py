from ai.core.celery_app import app
from ai.business.social2product.service import DifySocial2ProductService
import time

@app.task
def amz_to_ali_src(event):
    print("task: amz_to_ali_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    out_event['result'] = {'name': 'amz_to_ali_src'}
    return out_event

@app.task
def amz_to_1688_src(event):
    print("task: amz_to_1688_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    out_event['result'] = {'name': 'amz_to_1688_src'}
    return out_event

@app.task
def _1688_to_1688_src(event):
    print("task: _1688_to_1688_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    out_event['result'] = {'name': '_1688_to_1688_src'}
    return out_event

@app.task
def ali_to_ali_src(event):
    print("task: ali_to_ali_src, event:", event)
    out_event = event.copy()
    out_event['result'] = {'name': 'ali_to_ali_src'}
    time.sleep(5)
    return out_event

@app.task
def social_to_ali_src(event):
    print("task: social_to_ali_src, event:", event)

    payload = {
        "platform": event['context']['platform'],
        "page": event['context']['page'],
        "page_size": event['context']['page_size'],
        "trace_id": event['trace_id']
    }

    # 获取社媒信息
    service = DifySocial2ProductService()
    items = service.social_to_ali_src(payload)

    out_event = event.copy()
    out_event['result'] = {'items': items}

    return out_event 