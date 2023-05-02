from django.urls import path
from .views import GroupListView
from .views import GroupDetailView
from members.views import RequestMembership, RemoveMember
from groupchat.views import GroupChatList

urlpatterns = [
    path('', GroupListView.as_view()),
    path('', GroupDetailView.as_view()),
    path('<int:pk>/', GroupDetailView.as_view()),
    path('<int:pk>/join/', RequestMembership.as_view()),
    path('<int:pk>/groupchat/', GroupChatList.as_view()),
    path('<int:group_pk>/<int:member_pk>/remove/', RemoveMember.as_view()),
    path('<int:group_pk>/leavegroup/', RemoveMember.as_view()),
]
