import os
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

TELEGRAM_TOKEN = os.getenv("8101896389:AAEMwjBctSEIKbcNL0ZdvybJQ7qQbtSCqOY")
VK_TOKEN = os.getenv("vk1.a.zmOnoN3GVndI-X6SavZkIaEhrXQK3GAkIVo2uqJdvfI43h9BFgU6SB_7qTQK6aawGm0qKmpE7lYJndxi1WPaHMBbutlMNDug6zm0-cy_l8ulkFq0nT3ejwqxwrybrhJc9_kC_lwKO6qldJ5KQRTqisZzCDpjlX5RipmICW56s-slgreLlcksFq0uY80P_IAbdjfABBhtuKMMgsy64EYg6A")
CHAT_IDS = os.getenv("1243372999", "").split(",")

GROUP_ID = int(os.getenv("211587219")) 

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
