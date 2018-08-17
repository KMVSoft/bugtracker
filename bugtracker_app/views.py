from textwrap import shorten

import requests

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from bugtracker_app.models import IssueForm
from bugtracker_app.models import Setting

from . import email_utils
from . import redmine

APP_NAME = 'bugtracker'
setting = Setting.load()

class Index(TemplateView):
    template_name = APP_NAME+'/index.html'

    def post(self, request):
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            r = redmine.create_issue(
                setting.project_id,
                issue.subject,
                issue.description,
                1
            )
            print('!!!###', r)
            issue.id = int(r['issue']['id'])
            issue.save()
            return self.get(request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = IssueForm()
        return ctx

class ReportIssue(TemplateView):
    template_name = APP_NAME+'/report_issue.html'
    def post(self, request):
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return self.get(request)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = IssueForm()
        return ctx

class NewMessagesList(ListView):
    template_name = APP_NAME+'/new_messages_list.html'

    def get_queryset(self):
        return email_utils.get_unread_messages()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['issue_list'] = email_utils.parse_messages(email_utils.get_unread_messages())
        return ctx