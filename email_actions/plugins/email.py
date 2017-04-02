import logging

from smtplib import SMTP, SMTPHeloError, SMTPAuthenticationError, \
  SMTPNotSupportedError, SMTPException, SMTPRecipientsRefused,\
  SMTPSenderRefused, SMTPDataError

from email_actions.config import read_config_plugin

PLUGIN_NAME = 'email'


def email_notify(filter_name, msg_from, msg_to, msg_subject, msg_content):
  plugin_cfg = read_config_plugin(filter_name, PLUGIN_NAME)
  params = {
    'host': None,
    'port': 25,
    'username': None,
    'password': None,
    'secure': False
  }
  for key in plugin_cfg.keys():
    params[key] = plugin_cfg[key]

  if not params['host']:
    logging.error('Missing mandatory host config for email')
    return

  client = SMTP(params['host'], params['port'])
  send_mail = True
  if params['username'] and ['password']:
    if params['secure']:
      client.starttls()
    try:
      client.login(params['username'], params['password'])
    except (SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError,
            SMTPException) as e:
      send_mail = False
      logging.error('Error logging in to SMTP server: %s' % (e))

  if send_mail:
    # TODO: Form message properly
    try:
      client.sendmail(msg_from, msg_to, msg_content)
    except (SMTPHeloError, SMTPNotSupportedError, SMTPRecipientsRefused,
            SMTPSenderRefused, SMTPDataError) as e:
      logging.error('Error sending email: %s' % (e))

  client.quit()
