from ai.core.celery_app import app
from ai.business.social2product.service import DifySocial2ProductService
import time
import json
@app.task
def amz_to_ali_listing(event):
    print("task: amz_to_ali_listing, event:", event)
    out_event = event.copy()
    time.sleep(30)
    return out_event

@app.task
def amz_to_1688_listing(event):
    print("task: amz_to_1688_listing, event:", event)
    out_event = event.copy()
    time.sleep(30)
    return out_event

@app.task
def _1688_to_1688_listing(event):
    print("task: _1688_to_1688_listing, event:", event)
    out_event = event.copy()
    time.sleep(30)
    return out_event

@app.task
def ali_to_ali_listing(event):
    print("task: ali_to_ali_listing, event:", event)
    out_event = event.copy()
    time.sleep(30)
    return out_event

@app.task
def social_to_ali_listing(event):
    print(f"task: social_to_ali_listing, page: {event['context']['page']}, items count: {len(event['result']['items'])}")

    try:
        payload = {
            "items": json.dumps(event['result']['items'])
        }

        # 获取社媒信息
        service = DifySocial2ProductService()
        items = service.social_to_ali_listing(payload)

        out_event = event.copy()
        out_event['result'] = {'items': items}

        return out_event
    except Exception as e:
        print(f"Error in social_to_ali_listing: {str(e)}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        raise 