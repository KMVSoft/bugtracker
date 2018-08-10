from django.db import models
from django.forms import ModelForm

class IssueArea(models.Model):
    name = models.CharField(max_length=100, unique=True)

class IssueStatus(models.Model):
    name = models.CharField(max_length=30, unique=True)

class IssueImportance(models.Model):
    priority = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=30, unique=True)

class Issue(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    author_email = models.EmailField()
    author_name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    # FK
    status = models.ForeignKey(
        IssueStatus,
        on_delete=models.PROTECT)
    importance = models.ForeignKey(
        IssueImportance,
        on_delete=models.PROTECT)
    area = models.ForeignKey(
        IssueArea,
        on_delete=models.PROTECT)

# FORMS

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'body', 'author_name',
         'author_email', 'status', 'importance', 'area']
