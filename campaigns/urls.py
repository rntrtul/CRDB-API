from django.urls import path
from . import views

app_name = 'campaigns'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  # REST API URLs
  path('api/campaign', views.CampaignList.as_view()),
  path('api/campaign/<int:pk>/', views.CampaignDetail.as_view()),
]