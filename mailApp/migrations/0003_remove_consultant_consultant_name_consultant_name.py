# Generated by Django 5.0.6 on 2024-07-19 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailApp', '0002_remove_consultant_email_remove_consultant_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultant',
            name='consultant_name',
        ),
        migrations.AddField(
            model_name='consultant',
            name='name',
            field=models.CharField(default='SOMESTRING', max_length=100),
        ),
    ]
