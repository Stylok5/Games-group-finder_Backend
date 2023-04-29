from django.urls import path
from .views import GroupChatList

urlpatterns = [
    path('groups/<int:pk>/groupchat/', GroupChatList.as_view()),
]
