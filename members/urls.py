from django.urls import path
from .views import RequestMembership, RemoveMember

urlpatterns = [
    path('groups/<int:pk>/join/', RequestMembership.as_view()),
    path('groups/<int:group_pk>/<int:member_pk>/remove/',
         RemoveMember.as_view()),
    path('<int:group_pk>/leavegroup/', RemoveMember.as_view()),
]
