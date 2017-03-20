import os
import logging
import configparser

cfg = None


def create_config(path):
  cfg = configparser.ConfigParser()
  cfg['Plugin: Join'] = {
    'API_KEY': ''
  }

  try:
    with open(path, "w") as config_file:
      cfg.write(config_file)
  except IOError as e:
    logging.critical('Error while writing config_file %s: %s'
                     % (path, str(e)))
    logging.critical('Check the config file path and try again')
    return False
  return True


def check_config(path):
  if not os.path.exists(path):
    logging.warning('Config file %s doesn\'t exist. Trying to create'
                    % (path))
    if create_config(path):
      logging.warning('Created new config file %s. Edit it first to '
                      'configure your settings correctly & then run '
                      'program again' % (path))
    return False
  else:
    global cfg
    cfg = configparser.ConfigParser()
    try:
      with open(path, "r") as config_file:
        cfg.read_file(config_file)
    except IOError as e:
      logging.critical('Error while reading config_file %s: %s'
                       % (path, str(e)))
      logging.critical('Check the config file path and try again')
      return False
  return True


def read_config_plugin(plugin_name):
  return cfg['Plugin: ' + plugin_name]
