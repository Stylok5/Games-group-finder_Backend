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
                return Response({'error': 'You have already liked this group'}, status=status.HTTP_400_BAD_REQUEST)
            rating.likes += 1
            rating.has_liked = True

            if rating.has_disliked:
                rating.has_disliked = False
                rating.dislikes -= 1

            rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(
                group=group, user=user, likes=1, has_liked=True)

        # update the group likes and dislikes count
        group.likes += 1
        group.dislikes -= 1 if rating.has_disliked else 0
        group.save()

        # return the updated user likes count
        user_likes = rating.likes if hasattr(rating, 'likes') else 0
        return Response({'user_likes': user_likes, 'group_likes': group.likes}, status=status.HTTP_200_OK)


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
                return Response({'error': 'You have already disliked this group'}, status=status.HTTP_400_BAD_REQUEST)
            rating.dislikes += 1
            rating.has_disliked = True

            if rating.has_liked:
                rating.has_liked = False
                rating.likes -= 1

            rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(
                group=group, user=user, dislikes=1, has_disliked=True)

        # update the group likes and dislikes count
        group.dislikes += 1
        group.likes -= 1 if rating.has_liked else 0
        group.save()

        # return the updated user likes count
        user_dislikes = rating.dislikes if hasattr(rating, 'dislikes') else 0
        return Response({'user_dislikes': user_dislikes, 'group_dislikes': group.dislikes}, status=status.HTTP_200_OK)
