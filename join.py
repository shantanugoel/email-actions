import requests
import logging

from config import JOIN_API_KEY

BASE_URL = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?'


def join_notify(msg_from, msg_to, msg_subject, msg_content):
  params = {
    'deviceId': 'group.all',
    'title': msg_subject,
    'text': msg_content,
    'apikey': JOIN_API_KEY
  }
  logging.debug("Sending notification to %s" % (params['deviceId']))
  requests.get(BASE_URL, params=params)
