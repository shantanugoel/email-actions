from join import join_notify

def action(msg_from, msg_to, msg_subject, msg_content):
  join_notify(msg_from, msg_to, msg_subject, msg_content)
