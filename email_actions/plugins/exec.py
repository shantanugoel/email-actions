from subprocess import Popen
import logging

from email_actions.config import read_config_plugin

PLUGIN_NAME = 'exec'


def exec_notify(filter_name, msg_from, msg_to, msg_subject, msg_content):
  params = {
    'cmd': None,
    'args': [],
    'env': {
      'EA_ENV_MSG_FROM': msg_from,
      'EA_ENV_MSG_TO': msg_to,
      'EA_ENV_MSG_SUBJECT': msg_subject,
      'EA_ENV_MSG_CONTENT': msg_content,
    }
  }

  plugin_cfg = read_config_plugin(filter_name, PLUGIN_NAME)
  for key in plugin_cfg.keys():
    if key == 'env':
      try:
        for env_key in plugin_cfg[key].keys():
            params[key][env_key] = plugin_cfg[key][env_key]
      except:
        # Ignore stray env element in config without any actual env param
        pass
    else:
      params[key] = plugin_cfg[key]

  if not params['cmd']:
    logging.error('No command specified for plugin %s' % (PLUGIN_NAME))
    return

  popen_args = [params['cmd']]
  for arg in params['args']:
    popen_args.append(arg)
  Popen(popen_args, env=params['env'])
