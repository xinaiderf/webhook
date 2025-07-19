from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import uvicorn
import asyncio

# Configuração do Chrome (modo normal, não headless)
chrome_options = Options()
# chrome_options.add_argument("--headless=new")  # REMOVA ou COMENTE ESTA LINHA
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")  # Opcional
chrome_options.add_argument("--no-sandbox")   # Opcional para Linux

app = FastAPI()

driver = webdriver.Chrome(options=chrome_options)

# Evento para sincronizar o recebimento do webhook
webhook_event = asyncio.Event()
webhook_data = None

driver.get('https://clip.opus.pro/auth/oauth/login')
time.sleep(5)

email = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div/div/div/div[2]/div[1]/div/form/div/div/div/input')
email.send_keys('jovisire3@gmail.com')
time.sleep(5)

botao = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div/div/div/div[2]/div[1]/div/form/div/button')
botao.click()
time.sleep(5)

### WEBHOOK DO N8N ###

# Modelo do corpo do webhook
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



driver.quit()