# telegram_reminder.py - SEND ONLY (no polling, no conflict with Nanobot)
import os
import time
import requests
from datetime import datetime

# Read environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def _is_configured():
    return bool(BOT_TOKEN and CHAT_ID)


def send_telegram_message(message):
    """Send a message via Telegram Bot API."""
    if not _is_configured():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Telegram not configured")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Sent")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Exception: {e}")
        return False


def main():
    global BOT_TOKEN, CHAT_ID
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    print("🤖 小安 Telegram 提醒服務 (只發送)")
    print("📱 訊息將會傳送到你的 Telegram")
    print("-" * 40)

    if not _is_configured():
        print("⚠️ TELEGRAM_BOT_TOKEN and/or TELEGRAM_CHAT_ID are not set.")
        print("   Please set them in start_bot.cmd or environment variables.")
        return

    print("\n🧪 傳送測試訊息...")
    send_telegram_message("🧪 測試：小安提醒系統已經運作！你收到這個訊息代表成功！🎉")

    last_sent = {}

    while True:
        now = datetime.now()
        current_time = f"{now.hour:02d}:{now.minute:02d}"

        if current_time in last_sent:
            time.sleep(30)
            continue

        # 8:00 AM - Morning check-in
        if now.hour == 8 and now.minute == 0:
            send_telegram_message("🌅 早安！昨晚睡得好嗎？1-5分你會給多少？")
            last_sent[current_time] = True

        # 9:00 AM - Medication reminder
        elif now.hour == 9 and now.minute == 0:
            send_telegram_message("💊 小安提醒：現在是9:00，你應該服用多奈哌齊 5mg。已經服用了嗎？")
            last_sent[current_time] = True

        # 11:00 AM - Mid-morning check-in
        elif now.hour == 11 and now.minute == 0:
            send_telegram_message("☕ 小安問候你！現在11點，今天過得怎麼樣？有沒有什麼想跟我聊聊？")
            last_sent[current_time] = True

        # 3:00 PM - Cognitive reminder
        elif now.hour == 15 and now.minute == 0:
            send_telegram_message("🧠 小安想跟你做一個5分鐘的記憶練習，有興趣嗎？（回覆「好」/「不好」）")
            last_sent[current_time] = True

        # 9:00 PM - Evening check-in
        elif now.hour == 21 and now.minute == 0:
            send_telegram_message("🌙 晚安！今天過得怎麼樣？有什麼開心的事情可以分享？")
            last_sent[current_time] = True

        # Clean up old entries
        if len(last_sent) > 10:
            keys = list(last_sent.keys())
            for key in keys[:-10]:
                del last_sent[key]

        time.sleep(30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 提醒服務已停止。")