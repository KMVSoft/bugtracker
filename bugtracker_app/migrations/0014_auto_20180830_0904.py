# Generated by Django 2.1 on 2018-08-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker_app', '0013_auto_20180830_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='author_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
