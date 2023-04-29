from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers.populated import PopulatedGameSerializer
from .serializers.common import GameSerializer
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination


class GameListView(APIView):
    def get(self, request):
        page = request.GET.get('page')
        if page:
            games = Game.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 10  # number of games per page
            result_page = paginator.paginate_queryset(games, request)
            serialized_products = GameSerializer(result_page, many=True)
            return paginator.get_paginated_response(serialized_products.data)
        else:
            games = Game.objects.all()
            serialized_products = GameSerializer(games, many=True)
            return Response(serialized_products.data, status=status.HTTP_200_OK)

    def post(self, request):
        game_to_add = GameSerializer(data=request.data)
        try:
            game_to_add.is_valid()
            game_to_add.save()
            return Response(game_to_add.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GameDetailView(APIView):

    def get_game(self, _request, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise NotFound(
                detail="Can not find a game with that primary key")

    def get(self, request, pk):  # Add the request argument
        game = self.get_game(request, pk=pk)  # Pass the request argument
        serialized_game = PopulatedGameSerializer(game)
        return Response(serialized_game.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        game_to_edit = self.get_game(request, pk=pk)
        updated_game = GameSerializer(game_to_edit, data=request.data)
        try:
            updated_game.is_valid()
            updated_game.save()
            return Response(updated_game.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            res = {"detail": "Unprocessable Entity"}
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        game_to_delete = self.get_game(request, pk=pk)
        game_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
