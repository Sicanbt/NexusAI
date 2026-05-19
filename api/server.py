from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio

from nexus.core.orchestrator import Orchestrator
from nexus.core.config import NexusConfig

app = FastAPI(
    title="NexusAI API",
    description="Multi-Agent Autonomous Research & Decision Intelligence",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    task: str
    model: Optional[str] = "openai/gpt-4o"
    enable_validator: Optional[bool] = True
    max_reasoning_steps: Optional[int] = 32


class TaskResponse(BaseModel):
    report: str
    confidence: float
    reasoning_steps: int
    tokens_used: int


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/run", response_model=TaskResponse)
async def run_task(req: TaskRequest):
    config = NexusConfig(
        model=req.model,
        enable_validator=req.enable_validator,
        max_reasoning_steps=req.max_reasoning_steps,
        stream=False,
    )
    orchestrator = Orchestrator(config)
    try:
        result = await orchestrator.run(req.task)
        return TaskResponse(
            report=result if isinstance(result, str) else result.report,
            confidence=0.85,
            reasoning_steps=req.max_reasoning_steps,
            tokens_used=0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/run")
async def websocket_run(websocket: WebSocket):
    """Stream agent reasoning in real-time via WebSocket."""
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        task = data.get("task", "")
        if not task:
            await websocket.send_json({"error": "task is required"})
            return

        config = NexusConfig(stream=True)
        orchestrator = Orchestrator(config)

        await websocket.send_json({"event": "start", "task": task})
        report = await orchestrator.run(task)
        await websocket.send_json({"event": "done", "report": report})
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"event": "error", "detail": str(e)})
