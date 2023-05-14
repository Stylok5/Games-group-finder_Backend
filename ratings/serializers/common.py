from rest_framework import serializers
from ..models import Rating


class RatingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'
