from ai.core.celery_app import app
import time

@app.task
def amz_to_ali_image(event):
    print("task: amz_to_ali_image, event:", event)
    out_event = event.copy()
    time.sleep(50)
    out_event['result'] = {'name': 'amz_to_ali_image'}
    return out_event

@app.task
def amz_to_1688_image(event):
    print("task: amz_to_1688_image, event:", event)
    out_event = event.copy()
    time.sleep(50)
    out_event['result'] = {'name': 'amz_to_1688_image'}
    return out_event

@app.task
def _1688_to_1688_image(event):
    print("task: _1688_to_1688_image, event:", event)
    out_event = event.copy()
    time.sleep(50)
    out_event['result'] = {'name': '_1688_to_1688_image'}
    return out_event

@app.task
def ali_to_ali_image(event):
    print("task: ali_to_ali_image, event:", event)
    out_event = event.copy()
    time.sleep(50)
    out_event['result'] = {'name': 'ali_to_ali_image'}
    return out_event

@app.task
def social_to_ali_image(event):
    print(f"task: social_to_ali_image, page: {event['context']['page']}, items count: {len(event['result']['items'])}")
    out_event = event.copy()
    return out_event 