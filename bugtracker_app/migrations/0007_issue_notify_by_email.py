# Generated by Django 2.0.2 on 2018-08-17 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker_app', '0006_auto_20180817_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='notify_by_email',
            field=models.BooleanField(default=True),
        ),
    ]
