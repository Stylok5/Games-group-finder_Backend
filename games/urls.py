from django.urls import path
from .views import GameListView
from .views import GameDetailView

urlpatterns = [
    path('', GameListView.as_view()),
    path('<int:pk>/', GameDetailView.as_view()),
    path('pages/<int:page>/', GameListView.as_view(), {'page': 1}),
]
