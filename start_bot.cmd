@echo off
set TELEGRAM_BOT_TOKEN=8996713752:AAHSXj2D4rcU0bricN7KdLhjtrSWfxCdnp8
set TELEGRAM_CHAT_ID=1688453446

echo Starting nanobot gateway...
start "Gateway" py -3.14 -m nanobot gateway
timeout /t 3 /nobreak >nul

echo Starting Telegram reminder service...
start "Reminder" py -3.14 telegram_reminder.py

echo Both services are running!
pause