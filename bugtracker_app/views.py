import json

import requests
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import View

from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponse

from bugtracker_app.models import IssueForm
from bugtracker_app.models import RegisterForm
from bugtracker_app.models import Setting
from bugtracker_app.models import Issue
from bugtracker_app.models import IssueComment

from . import email_utils
from . import redmine
from . import utils
from .mymixins import CSRFExemptMixin


APP_NAME = 'bugtracker_app'

# Загружаем настройки
setting = Setting.load()

class Index(TemplateView):
    template_name = APP_NAME+'/index.html'

    def post(self, request):
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if request.user.is_authenticated:
                issue.author_name = request.user.first_name
                issue.author_email = request.user.email
                issue.author = request.user

            r = redmine.create_issue(issue)
            issue.id = r['issue']['id']
            issue.save()
            return self.get(request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = IssueForm()
        ctx['page_report'] = 'active' #for bs 3 navbar
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
    def post(self, request, pk):
        comment = request.POST.get('comment')
        header = setting.note_from_issue_author
        response = redmine.create_note(pk, header+comment)
        if response.status_code == 200:
            IssueComment.objects.create(
                content=comment,
                from_username=request.user.username,
                issue=self.get_object() 
                )
        return self.get(request, pk)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = APP_NAME+'/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_profile'] = 'active' #css class for BS 3 navbar
        ctx['comments'] = IssueComment.objects.filter(
            issue__author=self.request.user)
        # FIXIT HARDCODING status__name
        ctx['new'] = Issue.objects.filter(
            status__name='новая',
            author=self.request.user)
        ctx['in_progress'] = Issue.objects.filter(
            status__name='в работе')
        ctx['solved'] = Issue.objects.filter(
            status__name='решена',
            author=self.request.user)
        return ctx

class NoteAPI(CSRFExemptMixin, View):
    def post(self, request):
        api_key = str(setting.api_key).replace('-','')
        http_auth = request.META['HTTP_AUTHORIZATION']

        if http_auth != api_key:     
            return HttpResponseForbidden('api_key is not valid')

        data = json.loads(request.body.decode('utf-8'))
        try:
            IssueComment.objects.create(is_staff=True, **data)
        except Exception as e:
            return HttpResponseBadRequest(
                content='Error when processing creation comment '+str(e)
            )
        return HttpResponse('OK')

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

class SolvedIssuesView(ListView):
    paginate_by = 10
    template_name = APP_NAME+'/solved_issues.html'

    def get_queryset(self):
        return Issue.objects.filter(status__name='решена')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_solved'] = 'active' # for css class BS 3
        return ctx


class InProgressIssuesView(ListView):
    paginate_by = 10
    template_name = APP_NAME+'/in_progress_issues.html'

    def get_queryset(self):
        return Issue.objects.filter(status__name='в работе')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_in_progress'] = 'active' # for css class BS 3
        return ctx