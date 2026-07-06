import time
import requests
from datetime import datetime

# Your Telegram bot token and chat ID
BOT_TOKEN = "8996713752:AAHSXj2D4rcU0bricN7KdLhjtrSWfxCdnp8"
CHAT_ID = "1688453446"
last_update_id = 0

def send_telegram_message(message):
    """Send a message via Telegram Bot API directly."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Sent")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Exception: {e}")
        return False

def get_updates(offset=None):
    """Get new messages from Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 10, "offset": offset}
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get("result", [])
    except:
        pass
    return []

def handle_reply(message_text):
    """Handle user's reply to cognitive training reminder."""
    msg = message_text.lower().strip()
    
    if msg in ["好", "yes", "有興趣", "ok", "可以", "想", "做"]:
        send_telegram_message("🧠 好的！請記住這3個詞語：🍎 蘋果、🚌 巴士、🔴 紅色。1分鐘後我會問你！")
        time.sleep(60)
        send_telegram_message("⏰ 時間到！你記得哪3個詞語？試試看！")
        return True
    elif msg in ["不好", "no", "沒有興趣", "不想", "取消"]:
        send_telegram_message("😊 沒問題！你想做的時候隨時告訴我。")
        return True
    else:
        send_telegram_message("😊 如果你有興趣，可以告訴我『好』！如果不想，就說『不好』。")
        return False

def main():
    global last_update_id
    print("🤖 小安 Telegram 提醒服務 (含認知訓練)")
    print("📱 訊息將會傳送到你的 Telegram")
    print("-" * 40)
    
    # Test message
    print("\n🧪 傳送測試訊息...")
    send_telegram_message("🧪 測試：小安提醒系統已經運作！你收到這個訊息代表成功！🎉")
    
    last_sent = {}
    waiting_for_reply = False
    
    while True:
        now = datetime.now()
        current_time = f"{now.hour:02d}:{now.minute:02d}"
        
        # ============================================================
        # CHECK FOR USER REPLIES (Cognitive Training)
        # ============================================================
        updates = get_updates(offset=last_update_id + 1 if last_update_id else None)
        for update in updates:
            last_update_id = update["update_id"]
            if "message" in update and "text" in update["message"]:
                user_msg = update["message"]["text"]
                
                # If user manually says "認知訓練" or "記憶練習"
                if "記憶練習" in user_msg or "認知訓練" in user_msg:
                    send_telegram_message("🧠 好的！請記住這3個詞語：🍎 蘋果、🚌 巴士、🔴 紅色。1分鐘後我會問你！")
                    time.sleep(60)
                    send_telegram_message("⏰ 時間到！你記得哪3個詞語？試試看！")
                    waiting_for_reply = False
                elif waiting_for_reply:
                    handle_reply(user_msg)
                    waiting_for_reply = False
        
        # ============================================================
        # SCHEDULED REMINDERS
        # ============================================================
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
            send_telegram_message("🧠 小安想跟你做一個5分鐘的記憶練習，有興趣嗎？")
            last_sent[current_time] = True
            waiting_for_reply = True
        
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