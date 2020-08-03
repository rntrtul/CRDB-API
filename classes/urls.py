from django.urls import path
from . import views

app_name = 'classes'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  #REST API URLs
  path ('api/class', views.ClassList.as_view()),
  path ('api/class/<int:pk>', views.ClassDetail.as_view()),
]