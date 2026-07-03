@echo off
echo Starting nanobot gateway...
start "Gateway" py -3.14 -m nanobot gateway
timeout /t 3 /nobreak >nul
echo Starting Telegram reminder service...
start "Reminder" py -3.14 telegram_reminder.py
echo Both services are running!
pause