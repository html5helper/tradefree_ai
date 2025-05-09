# ai/core/workflow_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid

from ai.core.event import Event
from ai.core.event_broker import EventBroker
from ai.core.workflow_state import WorkflowState

app = FastAPI(title="Event-Driven Workflow API")

class RunRequest(BaseModel):
    workflow: str
    payload: Dict[str, Any]
    context: Optional[Dict[str, Any]] = {}

class RunResponse(BaseModel):
    trace_id: str

class StatusResponse(BaseModel):
    trace_id: str
    workflow: str
    status: str
    tasks: Dict[str, Any]

@app.post("/workflows/run", response_model=RunResponse)
async def run_workflow(req: RunRequest):
    trace_id = str(uuid.uuid4())
    # 构造根事件
    ev = Event.create(req.workflow, req.payload, {"workflow": req.workflow, **req.context})
    ev["trace_id"] = trace_id
    # 注册 workflow
    WorkflowState.create_workflow(trace_id, req.workflow, ev)
    # 发布到调度
    EventBroker.publish(ev)
    return RunResponse(trace_id=trace_id)

@app.get("/workflows/{trace_id}/status", response_model=StatusResponse)
async def get_status(trace_id: str):
    wf = WorkflowState.get_workflow(trace_id)
    if not wf:
        raise HTTPException(status_code=404, detail="trace_id not found")
    return StatusResponse(
        trace_id=trace_id,
        workflow=wf["event_type"],
        status=wf["status"],
        tasks=WorkflowState.get_tasks(trace_id)
    )