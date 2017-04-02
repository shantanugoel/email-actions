import logging


from email_actions.config import get_filter_list, get_filter_rules,\
  get_actions_list
from email_actions.plugins import entry_funcs


class Filter():

  filters_list = []
  actions = {}

  def __init__(self):
    self.filters_list = get_filter_list()
    self._generate_actions_list()

  def _generate_actions_list(self):
    self.actions = entry_funcs

  '''
  Match the given input to the rules specified in config. It returns True
  unless any of the rules mismatch.
  '''
  def _match_rules(self, rules, msg_from, msg_to, msg_subject, msg_content):
    match_result = True
    for rule in rules.keys():
      rule_ignored = False
      if str.lower(rule) == 'to':
        if rules[rule] != msg_to:
          logging.debug('Rule being compared to %s' % (msg_to))
          match_result = False
      else:
        rule_ignored = True
        logging.warning('Ignoring unsupported rule %s' % (rule))

      if not rule_ignored:
        if match_result:
          logging.debug('Rule matched \'%s\': \'%s\'' % (rule, rules[rule]))
        else:
          logging.debug('Rule failed \'%s\': \'%s\'' % (rule, rules[rule]))
          break
    return match_result

  def filter(self, msg_from, msg_to, msg_subject, msg_content):
    logging.debug("Received message from %s" % (msg_from))
    for filter_name in self.filters_list:
      rules = get_filter_rules(filter_name)
      if self._match_rules(rules, msg_from, msg_to, msg_subject, msg_content):
        actions_list = get_actions_list(filter_name)
        for action in actions_list:
          logging.debug('Running action %s for filter %s' %
                        (action, filter_name))
          if action in self.actions:
            self.actions[action](filter_name, msg_from, msg_to, msg_subject,
                                 msg_content)
          else:
            logging.warning('Unsupported Action %s specified for Filter %s' %
                            (action, filter_name))
