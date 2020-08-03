from django.urls import path
from . import views

app_name = 'races'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  # REST API URLs
  path ('api/race', views.RaceList.as_view()),
  path ('api/race/<int:pk>', views.RaceDetail.as_view()),
]