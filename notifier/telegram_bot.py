import requests
from config import BOT_TOKEN, CHAT_ID

def send_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram bot token or chat ID not configured.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def send_job(job, score):
    message = (
        f"🚀 *Backend Job Alert*\n\n"
        f"*Company:* {job['company']}\n"
        f"*Role:* {job['title']}\n"
        f"*Location:* {job['location']}\n"
        f"*Score:* {score}\n\n"
        f"[Apply Here]({job['url']})"
    )
    send_message(message)
