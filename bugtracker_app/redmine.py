import requests

from .models import Setting

setting = Setting.load()

def get_id_of_custom_field(name:str):
    '''Получает id custom_field по его имени (name), в случае ошибки
    Возвращает отрицательное число, если не удалось сделать это'''
    r = requests.get(
        setting.redmine_url+'/custom_fields.json',
        params={'key':setting.redmine_api_access_key}
    )
    if r.status_code != 200:
        return -1;
    for field in r.json()['custom_fields']:
        if field['name'] == name:
            return field['id']
    return -2;

def create_issue(issue):
    '''Создаёт новую задачу в redmine, на вход передаётся объект модели задачи,
    если всё прошло удачно, возвращает созданный объект
    иначе вызывает исключение, вызывать в блоке try/except Exception as e'''
    get_id_of_custom_field('user_name')
    r = requests.post(
            setting.redmine_url+'/issues.json',
            json={
                'issue': {
                    "subject": issue.subject,
                    "description": issue.description,
                    "custom_fields":[
                        {"value": issue.author_email,
                         "name": "user_email",
                         "id": get_id_of_custom_field('user_email')},
                        {"value": issue.author_name,
                         "name": "user_name", 
                         "id": get_id_of_custom_field('user_name')},
                        {"value": issue.area.name,
                         "name": "issue_area", 
                         "id": get_id_of_custom_field('issue_area')},
                    ],
                    "priority_id": issue.importance.priority,
                },
                "project_id": setting.project_id,
            },
            params={'key':setting.redmine_api_access_key}
        )
    return r.json()

def create_note(issue_id:int, note:str):
    '''Создаёт новое замечание с текстом note,
     в журнале задачи c идентификатором issue_id,
     возвращает response запроса'''
    r = requests.put(
            setting.redmine_url+'/issues/%d.json' % issue_id,
            json={
            'issue': {
                'notes': note
                }
            },
            params={'key':setting.redmine_api_access_key}
        )
    return r

def get_issues_list():
    '''Возвращает список всех задач, которые есть в redmine
    если всё прошло удачно, возвращает список задач,
    иначе вызывает исключение, вызывать в блоке try/except Exception as e'''
    r = requests.get(
        setting.redmine_url+'/issues.json',
        params={'key':setting.redmine_api_access_key,
                'assigned_to_id': 1
        }       
    )
    return r.json()

def get_issue(id:int):
    '''Возвращает данные задачи из redmine по её идентификатору id
    если всё прошло удачно, возвращает данные задачи,
    иначе вызывает исключение, вызывать в блоке try/except Exception as e'''
    r = requests.get(
        setting.redmine_url+'/issues/%d.json' % id,
        params={'key':setting.redmine_api_access_key}       
    )
    return r.json()