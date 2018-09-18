import uuid
from textwrap import shorten

from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils.deconstruct import deconstructible
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


from . import models_default_values as mdv


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class IssueCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name        

class IssueArea(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

@deconstructible()
class IssueStatus(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(pk=1, name=mdv.status_name)

class IssueImportance(models.Model):
    priority = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return '%d - %s' % (self.priority, self.name)

class Issue(models.Model):
    subject = models.CharField(max_length=50)
    description = models.TextField()
    notify_by_email = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    # for anonymous users
    author_name = models.CharField(max_length=30, null=True, blank=True)
    author_email = models.EmailField(null=True, blank=True)

    # FK
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True)

    status = models.ForeignKey(
        IssueStatus,
        on_delete=models.PROTECT,
        default=IssueStatus.get_default()[0])

    importance = models.ForeignKey(
        IssueImportance,
        on_delete=models.PROTECT)
    
    area = models.ForeignKey(
        IssueArea,
        on_delete=models.PROTECT)

    category = models.ForeignKey(
        IssueCategory,
        on_delete=models.PROTECT,
        default=0)

    def __str__(self):
        return 'Subject: %s Descr: %s' % (self.subject,
                                shorten(self.description, width=128, placeholder='...'))

    def get_absolute_url(self):
        return reverse('bugtracker:issue_detail', args=(self.id,))


class IssueComment(models.Model):
    content = models.TextField()
    from_username = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    # FK
    issue = models.ForeignKey(
        Issue,
        on_delete=models.PROTECT)



class Setting(SingletonModel):
    #REDMINE SETTINGS 
    redmine_url = models.CharField(max_length=255, default=mdv.redmine_url)
    redmine_api_access_key = models.CharField(max_length=100)
    project_id = models.CharField(max_length=255)
    redmine_sync_every_mins = models.PositiveSmallIntegerField(
        default=720,
        help_text='Как часто будет происходить синхронизация с redmine'
    )

    #EMAIL SETTINGS 
    smtp_email_client_host = models.CharField(default=mdv.smtp_host, max_length=200)
    smtp_email_client_port = models.PositiveIntegerField(default=mdv.smtp_port)
    imap_email_client_host = models.CharField(default=mdv.imap_host, max_length=200)
    imap_email_client_port = models.PositiveIntegerField(default=mdv.imap_port)
    email_login = models.CharField(max_length=255)
    email_password = models.CharField(max_length=255)

    api_key = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return 'Setting'

# FORMS

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'description', 'author_name', 'category',
         'author_email', 'notify_by_email', 'importance', 'area']

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2', )