from django.urls import path
from . import views

app_name = 'spells'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('spellCast/<int:pk>/', views.CastDetailView.as_view(), name='castDetail'),
]