from . import redmine
from .models import Setting
from .models import Issue
from .models import IssueStatus

setting = Setting.load()

def update_issues():
	upd_tasks_list = []
	issues = Issue.objects.all()
	statuses = map(lambda s: s.name, IssueStatus.objects.all())
	for issue in issues:
		response = redmine.get_issue(issue.id)
		response_status = response['issue']['status']['name'].lower()
		issue_status = issue.status.name.lower()
		if response_status != issue_status and response_status in statuses:
			upd_status = IssueStatus.objects.get(name=response_status)
			issue.status = upd_status
			issue.save()