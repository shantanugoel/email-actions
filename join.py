import requests

from config import JOIN_API_KEY

BASE_URL = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?'

def join_notify(msg_from, msg_to, msg_subject, msg_content):
  deviceId = 'group.all'
  params = {
    'deviceId': 'group.all',
    'title': msg_subject,
    'text': msg_content,
    'apikey': JOIN_API_KEY
    }
  print("Sending notification")
  r = requests.get(BASE_URL, params=params)
