from django.urls import path
from . import views

app_name = 'campaigns'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  # REST API URLs
  path('api/campaign'           , views.CampaignViewSet.as_view({'get':'list'})),
  path('api/campaign/<int:pk>/' , views.CampaignViewSet.as_view({'get':'retrieve'})),
]