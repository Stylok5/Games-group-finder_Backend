from .common import GenreSerializer
from games.serializers.common import GameSerializer


class PopulatedGenreSerializer(GenreSerializer):
    games = GameSerializer(many=True)
