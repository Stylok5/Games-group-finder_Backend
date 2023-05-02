from .models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from .serializers.common import GroupSerializer
from .serializers.populated import PopulatedGroupSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from games.models import Game
from members.models import Member
from rest_framework.exceptions import ValidationError
# Create your views here.


class GroupListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, _request):
        groups = Group.objects.all()
        serialized_groups = GroupSerializer(groups, many=True)
        return Response(serialized_groups.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        game_title = request.data.get('title', None)
        game = Game.objects.get(title=game_title)
        request.data['game'] = game.id
        request.data["owner"] = request.user.id
        request.data["members"] = []
        group_to_add = GroupSerializer(data=request.data)

        try:
            group_to_add.is_valid()
            group_to_add.save()
            return Response(group_to_add.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except AssertionError as e:
            return Response({"error": "Group name already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except:
            return Response({"detail": "Unproccesible Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GroupDetailView(APIView):
    def get_group(self, _request, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise NotFound(
                detail="Can not find a group with that primary key")

    def get(self, request, pk):  # Add the request argument
        group = self.get_group(request, pk=pk)
        serialized_group = PopulatedGroupSerializer(group)
        return Response(serialized_group.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        group_to_edit = self.get_group(request, pk=pk)

        # Only update owner field if present in request body
        if 'owner' in request.data:
            request.data['owner'] = request.user.id

        if request.user != group_to_edit.owner:
            return Response({"detail": "Only the owner of the group can update it."}, status=status.HTTP_403_FORBIDDEN)

        request.data["members"] = group_to_edit.members.all(
        ).values_list('id', flat=True)
        updated_group = GroupSerializer(
            group_to_edit, data=request.data, partial=True)

        try:
            updated_group.is_valid(raise_exception=True)
            updated_group.save()
            return Response(updated_group.data, status=status.HTTP_202_ACCEPTED)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unproccesible Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        group_to_delete = self.get_group(request, pk=pk)

        # check if the current user is the owner of the group
        if request.user == group_to_delete.owner:
            group_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Only the owner of the group can delete it."}, status=status.HTTP_403_FORBIDDEN)
