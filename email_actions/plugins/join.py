import requests
import logging

from email_actions.config import read_config_plugin

PLUGIN_NAME = 'join'
BASE_URL = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?'


def join_notify(filter_name, msg_from, msg_to, msg_subject, msg_content):
  # Default configuration
  params = {
    'deviceId': 'group.all',
    'title': msg_subject,
    'text': msg_content,
    'apikey': None
  }
  plugin_cfg = read_config_plugin(filter_name, PLUGIN_NAME)
  for key in plugin_cfg.keys():
    params[key] = plugin_cfg[key]
  logging.debug("Sending notification to %s" % (params['deviceId']))
  try:
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    response = r.json()
    if not response['success']:
      logging.error("Error while sending notification: %s" %
                    (response['errorMessage']))
  except requests.exceptions.RequestException as e:
    logging.error("Error while sending notification: %s" % (e))
