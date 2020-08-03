from django.urls import path
from . import views

app_name = 'damage'
urlpatterns = [
  #REST API URLs
  path ('api/damage', views.DamageList.as_view()),
  path ('api/damage/<int:pk>', views.DamageDetail.as_view()),
]