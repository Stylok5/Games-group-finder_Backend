from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers.populated import PopulatedGenreSerializer
from .models import Genre
from rest_framework import status
# Create your views here.


class GenreListView(APIView):

    def get(self, _request):
        genres = Genre.objects.all()
        serialized_genres = PopulatedGenreSerializer(genres, many=True)
        return Response(serialized_genres.data, status=status.HTTP_200_OK)
