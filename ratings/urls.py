from django.urls import path
from .views import Like, Dislike

urlpatterns = [
    path('groups/<int:pk>/like/', Like.as_view()),
    path('groups/<int:pk>/dislike/', Dislike.as_view()),
]
