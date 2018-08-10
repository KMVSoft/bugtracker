from django.shortcuts import render
from django.views.generic import View
from bugtracker_app.models import IssueForm
# Create your views here.
APP_NAME = 'bugtracker'

class ReportIssue(View):
	def post(self, request):
		form = IssueForm(request.POST)
		if form.is_valid():
			issue = form.save()

	def get(self, request):
		form = IssueForm()
		return render(request, APP_NAME+'/report_issue.html', {'form': form})
