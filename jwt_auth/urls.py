from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import UserListView
from .views import UserDetailListView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailListView.as_view()),
    path('user/', UserDetailListView.as_view()),
]
