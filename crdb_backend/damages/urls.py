from django.urls import path
from . import views

app_name = 'damage'
urlpatterns = [
  #REST API URLs
  path ('api/damage'          , views.DamageViewSet.as_view({'get':'list'})),
  path ('api/damage/<int:pk>' , views.DamageViewSet.as_view({'get':'retrieve'})),
]