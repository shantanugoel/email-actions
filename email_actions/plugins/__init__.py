from .join import join_notify
from .email import email_notify
from .exec import exec_notify

entry_funcs = {
    'join': join_notify,
    'email': email_notify,
    'exec': exec_notify,
}
