import requests

from .models import Setting

setting = Setting.load()


def create_issue(project_id:str, subject:str, description:str, priority_id:int):
	r = requests.post(
                setting.redmine_url+'/issues.json',
                json={
                    'issue': {
                        "subject": subject,
                        "description": description,
                        "priority_id": priority_id,
                    },
                    "project_id": project_id,
                },
                params={'key':setting.redmine_api_access_key}
            )
	print('@@@###', r)

	return r.json()


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