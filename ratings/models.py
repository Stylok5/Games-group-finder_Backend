from django.db import models


class Rating(models.Model):
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        'jwt_auth.User',
        on_delete=models.CASCADE,
        related_name='ratings_user'
    )
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    has_liked = models.BooleanField(default=False)
    has_disliked = models.BooleanField(default=False)
