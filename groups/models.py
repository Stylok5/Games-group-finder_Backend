from django.db import models
from django.contrib.auth import get_user_model
from members.models import Member
User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)
    game = models.ForeignKey(
        'games.Game',
        related_name='groups',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        on_delete=models.CASCADE,
        related_name='created_groups'
    )
    members = models.ManyToManyField(
        'members.Member',
        related_name='members_group',
        blank=True
    )

    description = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.name} created by {self.owner}'
