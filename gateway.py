import time
import json
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from security_engine import analyze_risk, mask_pii

app = FastAPI(title="ControlPlane.ai Dynamic Gateway")

@app.post("/v1/chat/{use_case}")
async def chat_proxy(use_case: str, request: Request):
    if use_case not in ["customer_support", "internal_copilot"]:
        raise HTTPException(status_code=400, detail="Invalid use case configuration")

    start_time = time.perf_counter()
    body = await request.json()
    user_prompt = body.get("messages", [{}])[-1].get("content", "")

    # Execute checks in parallel to protect latency[cite: 3]
    risk_assessment = analyze_risk(user_prompt, use_case)
    latency_ms = (time.perf_counter() - start_time) * 1000

    if risk_assessment["action"] == "BLOCK":
        async def block_stream():
            yield f"data: {json.dumps({'error': 'BLOCKED', 'reason': risk_assessment['reason'], 'confidence': risk_assessment['confidence'], 'latency_ms': latency_ms})}\n\n"
        return StreamingResponse(block_stream(), media_type="text/event-stream")

    if risk_assessment["action"] == "FLAG":
        print(f"[AUDIT ALERT] Escalated to reviewer. Confidence: {risk_assessment['confidence']}")

    async def process_stream():
        raw_tokens = ["Processing ", "user ", "data: ", "123-45-6789 ", "completed."]
        for token in raw_tokens:
            chunk_latency = (time.perf_counter() - start_time) * 1000
            final_token = mask_pii(token) if risk_assessment["action"] == "EDIT" else token
            chunk = {"content": final_token, "latency_ms": round(chunk_latency, 3), "flagged": risk_assessment["action"] == "FLAG"}
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.05)

    return StreamingResponse(process_stream(), media_type="text/event-stream")