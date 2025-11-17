import os
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
VK_TOKEN = os.getenv("VK_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

GROUP_ID = int(os.getenv("GROUP_ID")) 

vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()

def send_telegram(text):
    for chat_id in CHAT_IDS:
        chat_id = chat_id.strip()
        if not chat_id:
            continue
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": text}
        )

print("Бот запущен...")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        msg_text = event.obj.message["text"]
        from_user = event.obj.message["from_id"]
        send_telegram(f"Новое сообщение в сообществе от {from_user}:\n\n{msg_text}")
