from django.db.utils import IntegrityError
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from groups.serializers.populated import PopulatedGroupSerializer
from .serializers.common import UserSerializer
from groups.models import Group
from rest_framework.exceptions import NotFound
from .serializers.populated import PopulatedUserSerializer

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            try:
                user_to_create.save()
                return Response({'message': 'Registration successful'}, status=status.HTTP_202_ACCEPTED)
            except IntegrityError:
                raise APIException(
                    {'message': 'User already exists'}, code=status.HTTP_409_CONFLICT)
        else:
            return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(
                detail="No user found with that email. Please Register.")

        if not user_to_login.check_password(password):
            raise PermissionDenied(detail="Invalid Credentials")

        dt = datetime.now() + timedelta(days=7)
        token = jwt.encode({'sub': user_to_login.id, 'exp': int(
            dt.strftime('%s'))}, settings.SECRET_KEY, algorithm='HS256')

        return Response({'token': token, 'message': f"Welcome back {user_to_login.username}"})


class UserListView(APIView):

    def get(self, request):

        users = User.objects.all()
        serialized_user = UserSerializer(users, many=True)
        return Response(serialized_user.data)


class UserDetailListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self, pk):
        try:
            return get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            raise NotFound(detail='User not found')

    def get(self, request, pk=None):
        if pk is not None:
            user = self.get_user(pk)
        else:
            user = request.user
        serialized_user = PopulatedUserSerializer(user)

        # get groups where user is a member
        member_groups = Group.objects.filter(members__user=user.id)

        # get groups where user is the owner
        owner_groups = Group.objects.filter(owner__id=user.id)

        # combine the two querysets
        groups = member_groups.union(owner_groups)

        serialized_groups = PopulatedGroupSerializer(groups, many=True)

        user_data = serialized_user.data
        user_data['groups'] = serialized_groups.data

        return Response(user_data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        if pk is not None:
            user = self.get_user(pk)
        else:
            user = request.user

        serializer = PopulatedUserSerializer(user, data=request.data)

        if serializer.is_valid():
            new_username = serializer.validated_data.get('username')
            if new_username != user.username and User.objects.filter(username=new_username).exists():
                return Response({'error': 'The username you entered is already taken. Please choose a different username.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'A user with that username already exists'}, status=status.HTTP_400_BAD_REQUEST)
