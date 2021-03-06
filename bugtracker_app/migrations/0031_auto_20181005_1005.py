# Generated by Django 2.1.1 on 2018-10-05 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker_app', '0030_auto_20181005_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuecomment',
            name='reply_to',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='replies', to='bugtracker_app.IssueComment'),
        ),
        migrations.AddField(
            model_name='issueversion',
            name='status',
            field=models.CharField(default='open', max_length=255),
            preserve_default=False,
        ),
    ]
