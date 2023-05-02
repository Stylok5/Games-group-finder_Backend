from rest_framework import serializers
from ..models import Member


class PopulatedMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    profile_image = serializers.CharField(source='user.profile_image')

    class Meta:
        model = Member
        fields = '__all__'
