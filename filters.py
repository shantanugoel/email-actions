import logging
from join import join_notify


def filter(msg_from, msg_to, msg_subject, msg_content):
  logging.debug("Received message from %s" % (msg_from))
  # TODO: Add rule filtering here
  join_notify('ex1', msg_from, msg_to, msg_subject, msg_content)
