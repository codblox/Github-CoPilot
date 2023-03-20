bot_api_key = "5902964913:AAFzl3yDBFyobZyaki07o6hdqfUbTdUZYuI"
bot_chat_id = "5446415202"

# Function to send message on Telegram
import requests
import json

def send_message(message):
    requests.get(f'https://api.telegram.org/bot{bot_api_key}/sendMessage?chat_id={bot_chat_id}&text={message}&parse_mode=HTML')
