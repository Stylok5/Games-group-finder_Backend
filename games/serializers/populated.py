from .common import GameSerializer
from groups.serializers.common import GroupSerializer
from genres.serializers.common import GenreSerializer


class PopulatedGameSerializer(GameSerializer):
    groups = GroupSerializer(many=True)
    genre = GenreSerializer(many=True)
