@echo off
title Xiao An MCI Chatbot - Launcher
color 0A

echo ============================================
echo 🚀 Xiao An MCI Chatbot - Starting ALL Services
echo ============================================
echo.

echo 📡 [1/3] Starting RAG Server (AI Brain)...
start "RAG Server" cmd /k "cd /d C:\Users\user\.nanobot && py -3.14 rag_server.py"

timeout /t 3 /nobreak >nul

echo 🌐 [2/3] Starting Nanobot Gateway + Reminder...
start "Gateway + Reminder" cmd /k "cd /d C:\Users\user\Desktop\nanobot-main-main5\nanobot-main && start_bot.cmd"

timeout /t 3 /nobreak >nul

echo 📊 [3/3] Starting Caregiver Dashboard...
start "Dashboard" cmd /k "cd /d C:\Users\user\Desktop\nanobot-main-main5\nanobot-main && py -3.14 -m streamlit run dashboard.py"

echo.
echo ============================================
echo ✅ ALL SERVICES STARTED!
echo ============================================
echo.
echo 📋 Services running:
echo   1. RAG Server        → http://localhost:5001
echo   2. Nanobot Gateway   → Telegram, WeChat, WebUI
echo   3. Reminder Service  → Scheduled messages
echo   4. Caregiver Dashboard → http://localhost:8501
echo.
echo 📱 Test on Telegram: Send "什麼是腦退化症？"
echo 📊 Open Dashboard: http://localhost:8501
echo.
echo ⚠️ Close each window individually or press Ctrl+C
echo ============================================
pause