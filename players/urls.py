from django.urls import path
from . import views

app_name = 'players'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  #REST API URLs
  path ('api/player'          , views.PlayerViewSet.as_view({'get':'list'})),
  path ('api/player/<int:pk>' , views.PlayerViewSet.as_view({'get':'retrieve'})),
]