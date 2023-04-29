from rest_framework import serializers
from ..models import GroupChat


class PopulatedGroupChatSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = GroupChat
        fields = ('id', 'created_by', 'message_text', 'created_at')
