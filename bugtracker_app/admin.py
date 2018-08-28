from django.contrib import admin
# models import
from bugtracker_app.models import Issue
from bugtracker_app.models import IssueArea
from bugtracker_app.models import IssueStatus
from bugtracker_app.models import IssueImportance
from bugtracker_app.models import IssueCategory
from bugtracker_app.models import Setting
# Register your models here.
admin.site.register(Issue)
admin.site.register(IssueArea)
admin.site.register(IssueStatus)
admin.site.register(IssueImportance)
admin.site.register(IssueCategory)
admin.site.register(Setting)