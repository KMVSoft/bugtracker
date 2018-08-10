from django.db import models
from django.forms import ModelForm

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

class IssueStatus(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

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
        on_delete=models.PROTECT)
    importance = models.ForeignKey(
        IssueImportance,
        on_delete=models.PROTECT)
    area = models.ForeignKey(
        IssueArea,
        on_delete=models.PROTECT)

class Setting(SingletonModel):
    redmine_host = models.CharField(max_length=255)
    redmine_port = models.CharField(max_length=255)
    redmine_api_access_key = models.CharField(max_length=100)
    imap_email_client_host = models.CharField(max_length=255)
    imap_email_client_port = models.PositiveIntegerField()
    email_login = models.CharField(max_length=255)
    email_password = models.CharField(max_length=255)

# FORMS

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'body', 'author_name',
         'author_email', 'status', 'importance', 'area']
