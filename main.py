from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import uvicorn

app = FastAPI()

# Variáveis globais
webhook_event = asyncio.Event()
webhook_data = None

class WebhookPayload(BaseModel):
    codigo: str
    status: str = None

@app.post("/webhook")
async def receber_webhook(payload: WebhookPayload):
    global webhook_data
    print("✅ Webhook recebido:", payload)
    webhook_data = payload
    webhook_event.set()
    return {"ok": True, "recebido": payload.codigo}

@app.get("/")
async def status():
    return {"status": "online"}

# Sem o bloqueio no startup!

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
