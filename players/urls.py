from django.urls import path
from . import views

app_name = 'players'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  #REST API URLs
  path ('api/player', views.PlayerList.as_view()),
  path ('api/player/<int:pk>', views.PlayerDetail.as_view()),
]