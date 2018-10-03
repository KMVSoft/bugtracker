import sys
import re
import smtplib
import datetime

from email.mime.text import MIMEText
from email.header    import Header

from imbox import Imbox

from .models import Setting
from django.contrib.auth.models import User

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
    
def send_comment_notify(comment):
    if comment.issue.notify_by_email:
        send_email(
            'Новый комментарий',
            setting.comment_mail_template.format(
                    issue_url=comment.issue.get_absolute_url(),
                    user_name=comment.issue.author_name,
                    company_name=setting.company_name,
                    comment_content=comment.content
            ),
            comment.issue.author_email
        )

def send_error_after_report_notify(user, err_msg):
    content = setting.error_after_report_template.format(
        user_id=user.id if user else 'anonym',
        time=datetime.datetime.now(),
        error_message=err_msg
    )
    # send content all admins
    for admin in User.objects.filter(is_staff=True):
        send_email(
            '!!! Ошибка на сайте',
            content,
            admin.email
        )

def logout():
    imap.logout()
