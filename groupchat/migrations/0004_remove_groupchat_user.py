# Generated by Django 4.2 on 2023-04-24 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupchat', '0003_alter_groupchat_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupchat',
            name='user',
        ),
    ]
