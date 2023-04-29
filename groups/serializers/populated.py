from .common import GroupSerializer
from members.serializer.populated import PopulatedMemberSerializer
from jwt_auth.serializers.common import UserSerializer
from groupchat.serializers.populated import PopulatedGroupChatSerializer
from rest_framework import serializers
from ..models import Group
from games.serializers.common import GameSerializer


class PopulatedGroupSerializer(GroupSerializer):
    game = serializers.CharField(source='game.title')
    # game = GameSerializer()
    owner = UserSerializer()
    members = PopulatedMemberSerializer(many=True)
    groupchat_messages = PopulatedGroupChatSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'
