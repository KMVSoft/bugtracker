import requests

from .models import Setting

setting = Setting.load()


def create_issue(project_id:str,
                 subject:str,
                 description:str,
                 author_name:str,
                 author_email:str,
                 issue_area:str,
                 priority_id:int):
    r = requests.post(
                setting.redmine_url+'/issues.json',
                json={
                    'issue': {
                        "subject": subject,
                        "description": description,
                        "custom_fields":[
                            {"value": author_email, "name": "user_email", "id": 1},
                            {"value": author_name, "name": "user_name", "id": 2},
                            {"value": issue_area, "name": "issue_area", "id": 3},
                        ],
                        "priority_id": priority_id,
                    },
                    "project_id": project_id,
                },
                params={'key':setting.redmine_api_access_key}
            )
    return r.json()

def create_note(issue_id:int, note:str):
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
	r = requests.get(
		setting.redmine_url+'/issues.json',
		params={'key':setting.redmine_api_access_key,
				'assigned_to_id': 1
		}		
	)
	return r.json()

def get_issue(id:int):
	r = requests.get(
		setting.redmine_url+'/issues/%d.json' % id,
		params={'key':setting.redmine_api_access_key}		
	)
	return r.json()