import requests

from config.settings import TG_TOKEN, TG_URL


def send_tg_message(chat_id, message):
    params = {"text": message, "chat_id": chat_id}
    requests.get(f"{TG_URL}{TG_TOKEN}/sendMessage", params=params)


