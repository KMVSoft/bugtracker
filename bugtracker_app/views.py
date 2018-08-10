from django.shortcuts import render
from django.views.generic import View
from bugtracker_app.models import IssueForm
from bugtracker_app.models import Setting
import requests
# Create your views here.
APP_NAME = 'bugtracker'
setting = Setting.load()

class ReportIssue(View):
	def post(self, request):
		form = IssueForm(request.POST)
		if form.is_valid():
			issue = form.save()
			r = requests.post(
				setting.redmine_host+':'+setting.redmine_port+'/issues.json',
				json={
					'issue': {
						"project_id": 1,
						"subject": issue.title,
						"description": issue.body,
						"priority_id": 4,
					}
				},
				params={'key':setting.redmine_api_access_key})
			return self.get(request)

	def get(self, request):
		form = IssueForm()
		return render(request, APP_NAME+'/report_issue.html', {'form': form})
