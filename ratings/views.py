from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from groups.models import Group
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Rating


class Like(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # check if the user has already rated this group
        try:
            rating = Rating.objects.get(group=group, user=user)
            if rating.has_liked:
                pass
            else:
                rating.likes += 1
                rating.has_liked = True
                rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(
                group=group, user=user, likes=1, has_liked=True)

        # update the group likes count
        group.likes += 1
        if rating.has_disliked:
            group.dislikes -= 1
            if group.dislikes < 0:  # check if dislikes count has reached zero
                group.likes -= abs(group.dislikes)
                group.dislikes = 0
        group.save()

        # return the updated user likes count
        return Response({'You liked the group' 'group_likes': group.likes}, status=status.HTTP_200_OK)


class Dislike(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # check if the user has already rated this group
        try:
            rating = Rating.objects.get(group=group, user=user)
            if rating.has_disliked:
                pass
            else:
                rating.dislikes += 1
                rating.has_disliked = True
                rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(
                group=group, user=user, dislikes=1, has_disliked=True)

        # update the group likes and dislikes count
        group.dislikes += 1
        if rating.has_liked:
            group.likes -= 1
            if group.likes < 0:  # check if likes count has reached zero
                group.dislikes -= abs(group.likes)
                group.likes = 0
        group.save()

        # return the updated user dislikes count
        return Response({'You disliked the group' 'group_dislikes': group.dislikes}, status=status.HTTP_200_OK)
