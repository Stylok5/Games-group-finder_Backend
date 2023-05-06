from rest_framework import serializers
from ..models import Group
from games.models import Game


class GroupSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())
    likes = serializers.IntegerField(required=False)
    dislikes = serializers.IntegerField(required=False)
    class Meta:
        model = Group
        fields = '__all__'
