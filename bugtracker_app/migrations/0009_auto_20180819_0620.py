# Generated by Django 2.1 on 2018-08-19 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker_app', '0008_auto_20180819_0608'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='bugtracker_app.IssueCategory'),
        ),
    ]
