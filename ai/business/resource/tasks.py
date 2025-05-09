from ai.core.celery_app import app
import time

@app.task
def amz_to_ali_src(event):
    print("task: amz_to_ali_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    return out_event

@app.task
def amz_to_1688_src(event):
    print("task: amz_to_1688_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    return out_event

@app.task
def _1688_to_1688_src(event):
    print("task: _1688_to_1688_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    return out_event

@app.task
def ali_to_ali_src(event):
    print("task: ali_to_ali_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    return out_event

@app.task
def social_to_ali_src(event):
    print("task: social_to_ali_src, event:", event)
    out_event = event.copy()
    time.sleep(5)
    return out_event 