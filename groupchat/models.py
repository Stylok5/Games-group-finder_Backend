from django.db import models
# Create your models here.


class GroupChat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'jwt_auth.User', on_delete=models.CASCADE, related_name='created_groupchat_messages')
    group = models.ForeignKey(
        'groups.Group', related_name='groupchat_messages', on_delete=models.CASCADE)
    message_text = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
