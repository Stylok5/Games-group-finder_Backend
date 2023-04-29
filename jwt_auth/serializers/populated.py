from groups.serializers.populated import PopulatedGroupSerializer
from jwt_auth.serializers.common import UserSerializer
from ..models import User
from groups.serializers.common import GroupSerializer
from groups.models import Group
from rest_framework import serializers


class PopulatedUserSerializer(UserSerializer):
    groups = GroupSerializer(many=True, required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ('id', 'profile_image', 'description',
                  'username', 'email', 'groups', 'discord_link')
        extra_kwargs = {
            'username': {'required': False},
        }
