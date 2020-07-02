from django.urls import path
from . import views

app_name = 'episodes'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('apperances/', views.ApperanceIndexView.as_view(), name='apperanceIndex'),
  path('apperances/<int:pk>', views.ApperanceDetailView.as_view(), name='apperanceDetail'),
]