# Generated by Django 4.2 on 2023-04-23 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('groups', '0003_alter_group_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members_group', to='members.member'),
        ),
    ]
