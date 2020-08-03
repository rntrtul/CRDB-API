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
  path ('api/potion'               , views.PotionViewSet.as_view({'get':'list'})),
  path ('api/potion/<int:pk>'      , views.PotionViewSet.as_view({'get':'retrieve'})),
  path ('api/potionusage'          , views.PotionUsageViewSet.as_view({'get':'list'})),
  path ('api/potionusage/<int:pk>' , views.PotionUsageViewSet.as_view({'get':'retrieve'})),
  path ('api/weapon'               , views.WeaponViewSet.as_view({'get':'list'})),
  path ('api/weapon/<int:pk>'      , views.WeaponViewSet.as_view({'get':'retrieve'})),
  path ('api/weapondamage'         , views.WeaponDamageViewSet.as_view({'get':'list'})),
  path ('api/weapondamage/<int:pk>', views.WeaponDamageViewSet.as_view({'get':'retrieve'})),
  path ('api/weaponusage'          , views.WeaponUsageViewSet.as_view({'get':'list'})),
  path ('api/weaponusage/<int:pk>' , views.WeaponUsageViewSet.as_view({'get':'retrieve'})),
  path ('api/weaponowned'          , views.WeaponOwnedViewSet.as_view({'get':'list'})),
  path ('api/weaponowned/<int:pk>' , views.WeaponOwnedViewSet.as_view({'get':'retrieve'})),
]