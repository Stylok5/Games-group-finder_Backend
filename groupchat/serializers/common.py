from rest_framework import serializers
from ..models import GroupChat
from jwt_auth.serializers.common import UserSerializer


class GroupChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupChat
        fields = '__all__'
