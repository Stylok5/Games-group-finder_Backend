from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from groups.models import Group
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Rating


class Like(APIView):
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
                # User has already liked this group, return an error
                return Response({'error': 'You have already liked this group'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # User has not yet rated this group, set has_liked to True
                rating.likes
                rating.has_liked = True
                rating.save()
        except Rating.DoesNotExist:
            # User has not yet rated this group, create a new rating instance and set has_liked to True
            rating = Rating.objects.create(
                group=group, user=user, has_liked=True)


class Dislike(APIView):
    def post(self, request, pk):
        user = request.user
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already rated this group
        try:
            rating = Rating.objects.get(group=group, user=user)
            if rating.has_disliked:
                # User has already disliked this group, return an error
                return Response({'error': 'You have already disliked this group'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # User has not yet rated this group, set has_disliked to True
                rating.has_disliked = True
                rating.save()
        except Rating.DoesNotExist:
            # User has not yet rated this group, create a new rating instance and set has_disliked to True
            rating = Rating.objects.create(
                group=group, user=user, has_disliked=True)

        # Update the likes and dislikes count of the group
        group.dislikes += 1
        if rating.has_liked:
            group.likes -= 1
        group.save()

        # Return the updated likes and dislikes count of the group
        return Response({'likes': group.likes, 'dislikes': group.dislikes}, status=status.HTTP_200_OK)
