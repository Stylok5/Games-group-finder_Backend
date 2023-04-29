from rest_framework import serializers
from ..models import Group
from games.models import Game


class GroupSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())

    class Meta:
        model = Group
        fields = '__all__'
