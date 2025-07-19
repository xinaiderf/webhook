from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import uvicorn
import asyncio

app = FastAPI()

# ✅ Variáveis globais para comunicação
webhook_event = asyncio.Event()
webhook_data = None

### WEBHOOK DO N8N ###

class WebhookPayload(BaseModel):
    codigo: str
    status: str = None

@app.post("/webhook")
async def receber_webhook(payload: WebhookPayload):
    global webhook_data
    print("Webhook recebido:", payload)
    webhook_data = payload
    webhook_event.set()
    return {"ok": True, "recebido": payload.codigo}

@app.on_event("startup")
async def aguardar_webhook():
    print("⏳ Aguardando o webhook...")
    await webhook_event.wait()
    print("✅ Webhook recebido, conteúdo:", webhook_data)

### WEBHOOK DO N8N ###

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2501)
