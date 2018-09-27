import requests

from .models import Setting

setting = Setting.load()


def create_issue(issue):
    r = requests.post(
            setting.redmine_url+'/issues.json',
            json={
                'issue': {
                    "subject": issue.subject,
                    "description": issue.description,
                    "custom_fields":[
                        {"value": issue.author_email, "name": "user_email", "id": 1},
                        {"value": issue.author_name, "name": "user_name", "id": 2},
                        {"value": issue.area.name, "name": "issue_area", "id": 3},
                    ],
                    "priority_id": issue.importance.priority,
                },
                "project_id": setting.project_id,
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