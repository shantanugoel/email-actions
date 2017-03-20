import logging
from join import join_notify


def action(msg_from, msg_to, msg_subject, msg_content):
  logging.debug("Received message from %s" % (msg_from))
  join_notify(msg_from, msg_to, msg_subject, msg_content)
