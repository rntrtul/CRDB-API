from django.urls import path
from . import views

app_name = 'rolls'
urlpatterns = [
  path ('', views.index, name='index'),
  path('<int:roll_id>/', views.detail, name='detail'),
]