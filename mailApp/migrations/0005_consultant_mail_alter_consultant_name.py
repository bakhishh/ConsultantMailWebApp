# Generated by Django 5.0.6 on 2024-07-22 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailApp', '0004_alter_consultant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultant',
            name='mail',
            field=models.EmailField(default='none', max_length=255),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='name',
            field=models.CharField(default='none', max_length=255),
        ),
    ]
