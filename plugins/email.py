import logging

from smtplib import SMTP

from config import read_config_plugin

PLUGIN_NAME = 'email'


def email_notify(filter_name, msg_from, msg_to, msg_subject, msg_content):
  plugin_cfg = read_config_plugin(filter_name, PLUGIN_NAME)
  params = {
    'host': None,
    'port': None,
    'username': None,
    'password': None,
  }
  for key in plugin_cfg.keys():
    params[key] = plugin_cfg[key]

  if not params['host'] or not params['port']:
    logging.error('Missing mandatory host/port config for email')
    return

  client = SMTP(params['host'], params['port'])
  send_mail = True
  if params['username'] and ['password']:
    try:
      client.login(params['username'], params['password'])
    # TODO: Better Error Handling and logging returned error
    except:
      send_mail = False
      logging.error('Error logging in to given SMTP server')

  if send_mail:
    # TODO: Error Handling
    # TODO: Form message properly
    client.sendmail(msg_from, msg_to, msg_content)

  client.quit()
