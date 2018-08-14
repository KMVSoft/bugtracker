import sys
import re

from imbox import Imbox

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

def parse_messages(messages:list) -> list:
	result = []
	for uid, msg in messages:
		match = re.search(
			setting.regex_to_parse_email, 
			msg.body['plain'][0])
		result.append({
			'status': match.group('status'),
			'description': match.group('description')
		})
	return result
