import sys
import re
import smtplib
from email.mime.text import MIMEText
from email.header    import Header

from imbox import Imbox

from .models import Setting

setting = Setting.load()

def login_imap():
    # imap = Imbox(setting.imap_email_client_host,
    #             port=setting.imap_email_client_port,
    #             username=setting.email_login,
    #             password=setting.email_password)
    return None

def login_smtp():
    smtp = smtplib.SMTP_SSL(setting.smtp_email_client_host, 
                            setting.smtp_email_client_port)
    smtp.ehlo()
    smtp.login(setting.email_login,
               setting.email_password)
    smtp.auth_plain()
    return smtp

imap = login_imap()

def get_unread_messages() -> list:
    '''возвращает список всех писем с пометкой непрочитано
    в формате [(uid, imap), ..., (uid, imap)]'''
    return list(imap.messages(unread=True))    

def parse_messages(messages:list) -> list:
    '''парсит из списка писем в формате [(uid, imap), ..., (uid, imap)]
    данные задачи и возвращет ввиде списка словарей [{'status': ...}, ..., ]'''
    result = []
    for uid, msg in messages:
        match = re.search(
            setting.regex_to_parse_email, 
            msg.body['plain'][0])
        result.append({
            'issue_number': 0,
            'status': match.group('status'),
            'description': match.group('description')
        })
    return result

def mark_read(messages:list):
    '''Отмечает все письма из списка как прочитанные'''
    for uid, msg in messages:
        imap.mark_seen(uid)

    
def send_email(subject:str, body:str, to_email:str):
    '''Отправляет письму по указанному email адресу'''
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = setting.email_login
    msg['To'] = to_email

    smtp = login_smtp()
    result = smtp.sendmail(setting.email_login, to_email, msg.as_string())
    smtp.quit()
    return result
    

def logout():
    imap.logout()
