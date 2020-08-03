from django.urls import path
from . import views

app_name = 'races'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  # REST API URLs
  path ('api/race'          , views.RaceViewSet.as_view({'get':'list'})),
  path ('api/race/<int:pk>' , views.RaceViewSet.as_view({'get':'retrieve'})),
]