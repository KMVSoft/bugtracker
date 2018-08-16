from django.db import models
from django.forms import ModelForm
from django.utils.deconstruct import deconstructible
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
        return cls.objects.get_or_create(pk=1, name='new')

class IssueImportance(models.Model):
    priority = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return '%d - %s' % (self.priority, self.name)

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
        on_delete=models.PROTECT,
        default=IssueStatus.get_default()[0])
    importance = models.ForeignKey(
        IssueImportance,
        on_delete=models.PROTECT)
    area = models.ForeignKey(
        IssueArea,
        on_delete=models.PROTECT)

    def __str__(self):
        return 'title: %s Descr: %s' % (self.title,
                                shorten(self.body, width=128, placeholder='...'))

class Setting(SingletonModel):
    redmine_url = models.CharField(max_length=255, default=mdv.redmine_url)
    redmine_api_access_key = models.CharField(max_length=100)
    project_id = models.CharField(max_length=255)

    smtp_email_client_host = models.CharField(default=mdv.smtp_host, max_length=200)
    smtp_email_client_port = models.PositiveIntegerField(default=mdv.smtp_port)

    email_login = models.CharField(max_length=255)
    email_password = models.CharField(max_length=255)

    def __str__(self):
        return 'Setting'

# FORMS

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'body', 'author_name',
         'author_email', 'status', 'importance', 'area']
