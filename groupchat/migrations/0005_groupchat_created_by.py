# Generated by Django 4.2 on 2023-04-24 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupchat', '0004_remove_groupchat_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupchat',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_groupchat_messages', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
