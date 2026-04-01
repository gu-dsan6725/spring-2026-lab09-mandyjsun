"""
FastAPI wrapper for the memory-enabled Agent.

Exposes /ping and /invocation endpoints with multi-tenant support.
Maintains one Agent instance per run_id in a session cache.
"""

import os
import uuid
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import Agent

load_dotenv()

app = FastAPI(
    title="Memory Agent API",
    description="Multi-tenant conversational agent with semantic memory",
    version="1.0.0",
)

# Session cache: run_id -> Agent instance
_session_cache: Dict[str, Agent] = {}


def _get_or_create_agent(user_id: str, run_id: str) -> Agent:
    """Get existing Agent for this session or create a new one."""
    if run_id not in _session_cache:
        api_key = (
            os.getenv("GROQ_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )
        _session_cache[run_id] = Agent(user_id=user_id, run_id=run_id, api_key=api_key)
    return _session_cache[run_id]


class InvocationRequest(BaseModel):
    user_id: str
    run_id: Optional[str] = None
    query: str
    metadata: Optional[Dict[str, Any]] = None


class InvocationResponse(BaseModel):
    response: str
    user_id: str
    run_id: str


@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Memory Agent API is running"}


@app.post("/invocation", response_model=InvocationResponse)
def invocation(req: InvocationRequest):
    run_id = req.run_id or str(uuid.uuid4())[:8]
    try:
        agent = _get_or_create_agent(req.user_id, run_id)
        response = agent.chat(req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return InvocationResponse(response=response, user_id=req.user_id, run_id=run_id)
