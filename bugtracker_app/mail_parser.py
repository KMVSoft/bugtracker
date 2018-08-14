from imbox import Imbox
import sys

from .models import Setting
setting = Setting.load()

def get_unread_messages() -> list:
    unread_messages = []
    with Imbox(setting.imap_email_client_host,
            port=setting.imap_email_client_port,
            username=setting.email_login,
            password=setting.email_password) as mail:
        unread_messages = list(mail.messages(unread=True))
    return unread_messages    