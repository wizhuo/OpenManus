from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
from app.agent.data_analysis_manus import DataAnalysisManus

app = FastAPI()

async def event_stream():
    """ 模拟 SSE 事件流 """
    count = 0
    while True:
        count += 1
        yield f"data: {{\"message\": \"Hello {count}\"}}\n\n"
        await asyncio.sleep(1)  # 模拟延迟

@app.get("/sse")
async def sse(prompt: str):
    agent = DataAnalysisManus()
    await agent.run(prompt)
    # return StreamingResponse(agent.run(prompt), media_type="text/event-stream")

# 运行: ` uvicorn api_server:app --reload`
