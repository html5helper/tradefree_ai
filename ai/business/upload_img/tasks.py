from ai.core.celery_app import app
import time

@app.task
def amz_to_ali_upload(event):
    print("task: amz_to_ali_upload, event:", event)
    out_event = event.copy()
    time.sleep(25)
    return out_event

@app.task
def amz_to_1688_upload(event):
    print("task: amz_to_1688_upload, event:", event)
    out_event = event.copy()
    time.sleep(25)
    return out_event

@app.task
def _1688_to_1688_upload(event):
    print("task: _1688_to_1688_upload, event:", event)
    out_event = event.copy()
    time.sleep(25)
    return out_event

@app.task
def ali_to_ali_upload(event):
    print("task: ali_to_ali_upload, event:", event)
    out_event = event.copy()
    time.sleep(25)
    return out_event

@app.task
def social_to_ali_upload(event):
    print(f"task: social_to_ali_upload, page: {event['context']['page']}, items count: {len(event['result']['items'])}")
    out_event = event.copy()
    return out_event 