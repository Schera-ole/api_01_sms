import time
import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    access_token = os.getenv("access_token")
    url = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": user_id,
        "v": "5.92",
        "fields": "online",
        "access_token": access_token,
    }
    status = requests.post(url, params=params)
    return status.json()["response"][0]["online"]


def sms_sender(sms_text):
    account_sid = os.getenv("account_sid")
    auth_token = os.getenv("auth_token")
    client = Client(account_sid, auth_token)
    number_from = os.getenv("NUMBER_FROM")
    number_to = os.getenv("NUMBER_TO")
    message = client.messages.create(body=sms_text, from_=number_from, to=number_to)
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f"{vk_id} сейчас онлайн!")
            break
        time.sleep(60)
