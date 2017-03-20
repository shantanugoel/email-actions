import requests
import logging

from config import read_config_plugin

PLUGIN_NAME = 'Join'
BASE_URL = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?'


def join_notify(msg_from, msg_to, msg_subject, msg_content):
  plugin_cfg = read_config_plugin(PLUGIN_NAME)
  params = {
    'deviceId': 'group.all',
    'title': msg_subject,
    'text': msg_content,
    'apikey': plugin_cfg['API_KEY']
  }
  logging.debug("Sending notification to %s" % (params['deviceId']))
  requests.get(BASE_URL, params=params)
