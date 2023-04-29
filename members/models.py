# Create your models here.
from django.db import models


class Member(models.Model):
    user = models.ForeignKey(
        'jwt_auth.User', related_name='groups_users', on_delete=models.CASCADE)

    group = models.ForeignKey(
        'groups.Group',
        related_name='members_group',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'group')
