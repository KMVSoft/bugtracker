import requests
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import View

from bugtracker_app.models import IssueForm
from bugtracker_app.models import RegisterForm
from bugtracker_app.models import Setting
from bugtracker_app.models import Issue

from . import email_utils
from . import redmine
from . import utils


APP_NAME = 'bugtracker_app'

# Pfuh
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
                issue.author_name,
                issue.author_email,
                issue.area.name,
                issue.importance.priority
            )
            issue.id = r['issue']['id']
            issue.save()
            return self.get(request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = IssueForm()
        # FIXIT HARDCODING status__name
        ctx['in_progress'] = Issue.objects.filter(status__name='в работе')
        ctx['solved'] = Issue.objects.filter(status__name='решена')
        return ctx

class UpdateStatus(TemplateView):
    template_name = APP_NAME+'/update_status.html'

    def post(self, request):
        utils.update_issues()
        return self.get(request)

class IssueDetail(DetailView):
    model = Issue

class NoteAPI(View):
    def post(self, request):
        pass

class RegisterView(TemplateView):
    template_name = 'registration/register.html'
    def post(self, request):
        form = RegisterView(request.POST)
        if form.is_valid():
            user_model = form.save()
            user = authenticate(
                username=user_model.username,
                password=user_model.password
            )
            login(request, user)
            return redirect('bugtracker:index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = RegisterForm()
        return ctx