from django.urls import path
from . import views

app_name = 'items'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('potion-usage/<int:pk>', views.PotionUsageDetailView.as_view(), name='potionUsageDetail'),
  path('weapons/', views.WeaponIndexView.as_view(), name='weaponIndex'),
  path('weapons/<int:pk>', views.WeaponDetailView.as_view(), name='weaponDetail'),
]