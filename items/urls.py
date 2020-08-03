from django.urls import path
from . import views

app_name = 'items'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('potion-usage/<int:pk>', views.PotionUsageDetailView.as_view(), name='potionUsageDetail'),
  path('weapons/', views.WeaponIndexView.as_view(), name='weaponIndex'),
  path('weapons/<int:pk>', views.WeaponDetailView.as_view(), name='weaponDetail'),
  # REST API URLs
  path ('api/potion', views.PotionList.as_view()),
  path ('api/potion/<int:pk>', views.PotionDetail.as_view()),
  path ('api/potionusage', views.PotionUsageList.as_view()),
  path ('api/potionusage/<int:pk>', views.PotionUsageDetail.as_view()),
  path ('api/weapon', views.WeaponList.as_view()),
  path ('api/weapon/<int:pk>', views.WeaponDetail.as_view()),
  path ('api/weapondamage', views.WeaponDamageList.as_view()),
  path ('api/weapondamage/<int:pk>', views.WeaponDamageDetail.as_view()),
  path ('api/weaponusage', views.WeaponUsageList.as_view()),
  path ('api/weaponusage/<int:pk>', views.WeaponUsageDetail.as_view()),
  path ('api/weaponowned', views.WeaponOwnedList.as_view()),
  path ('api/weaponowned/<int:pk>', views.WeaponOwnedDetail.as_view()),
]