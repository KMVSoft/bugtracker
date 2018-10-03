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
        if not form.is_valid():
            return self.get(request)

        issue = form.save(commit=False)
        if request.user.is_authenticated:
            issue.set_author(request.user)

        try:
            r = redmine.create_issue(issue)
            issue.id = r['issue']['id']
            issue.save()
        except Exception as e:
            email_utils.send_error_after_report_notify(request.user, e)
            return redirect('bugtracker:error_after_report')
        else:  
            request.session['report_issue_id'] = issue.id
            return redirect('bugtracker:thanks_for_report')
            

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = IssueForm()
        ctx['page_report'] = 'active' #for bs 3 navbar
        # FIXIT HARDCODING status__name
        ctx['in_progress'] = Issue.objects.filter(status__name='в работе')
        ctx['solved'] = Issue.objects.filter(status__name='решена')
        return ctx

class ThanksForReporteView(TemplateView):
    template_name = APP_NAME + '/alerts/thanks_for_report.html'

    def get(self, request):
        page = super().get(request)
        if request.session.get('report_issue_id'):
            self.request.session.pop('report_issue_id')
            return page
        else:
            return redirect('bugtracker:index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['report_issue_id'] = self.request.session.get('report_issue_id', None)
        return ctx

class ErrorAfterReportView(TemplateView):
    template_name = APP_NAME + '/alerts/error_after_report.html'

class UpdateStatus(TemplateView):
    template_name = APP_NAME+'/update_status.html'

    def post(self, request):
        utils.update_issues()
        return self.get(request)

class IssueDetail(DetailView):
    model = Issue
    # Add new comment
    def post(self, request, pk):
        comment_content = request.POST.get('comment')
        header = setting.note_from_issue_author
        response = redmine.create_note(pk, header+comment_content)
        if response.status_code == 200:
            comment = IssueComment.objects.create(
                content=comment_content,
                from_username=request.user.username,
                issue=self.get_object(),
                user=request.user  
            )
            if comment.issue.author == request.user:
                email_utils.send_comment_notify(comment)
        return self.get(request, pk)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = APP_NAME+'/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_profile'] = 'active' #css class for BS 3 navbar
        ctx['comments'] = IssueComment.objects.filter(
            issue__author=self.get_object()).exclude(
            user=self.get_object())
        ctx['my_comments'] = IssueComment.objects.filter(
            user=self.get_object())
        # FIXIT HARDCODING status__name
        ctx['new'] = Issue.objects.filter(
            status__name='новая',
            author=self.get_object())
        ctx['in_progress'] = Issue.objects.filter(
            status__name='в работе')
        ctx['solved'] = Issue.objects.filter(
            status__name='решена',
            author=self.get_object())
        return ctx

class NoteAPI(CSRFExemptMixin, View):
    def post(self, request):
        api_key = str(setting.api_key).replace('-','')
        http_auth = request.META['HTTP_AUTHORIZATION']

        if http_auth != api_key:     
            return HttpResponseForbidden('api_key is not valid')

        data = json.loads(request.body.decode('utf-8'))
        try:
            comment = IssueComment.objects.create(is_staff=True, **data)
            email_utils.send_comment_notify(comment)
        except Exception as e:
            return HttpResponseBadRequest(
                content='Error when processing creation comment '+str(e)
            )
        return HttpResponse('OK')

class RegisterView(TemplateView):
    template_name = 'registration/register.html'
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bugtracker:index')
        else:
            return self.get(request)

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