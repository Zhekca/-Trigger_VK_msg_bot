# -*- coding: utf-8 -*-

import time
import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests

TELEGRAM_TOKEN = "TELEGRAM_TOKEN"
VK_TOKEN = "VK_TOKEN"

CHAT_IDS = ["CHAT_IDS"] 
GROUP_ID = GROUP_ID       

vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()


def send_telegram(text):
    link = "https://vk.com/gim211587219"

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "Открыть", "url": link}
            ]
        ]
    }

    for chat_id in CHAT_IDS:
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": json.dumps(reply_markup)
            }
        )


print("Бот запущен...")


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        msg = event.obj.message
        msg_text = msg.get("text", "")
        from_user_id = msg.get("from_id", "")


        user_info = vk.users.get(user_ids=from_user_id)
        first_name = user_info[0].get("first_name", "")
        last_name = user_info[0].get("last_name", "")

        telegram_text = f"{first_name} {last_name}:\n{msg_text}"

        send_telegram(telegram_text)
