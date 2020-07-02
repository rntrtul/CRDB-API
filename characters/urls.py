from django.urls import path
from . import views

app_name = 'characters'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('types/', views.TypeListView.as_view(), name='typeIndex'),
  path('types/<int:pk>', views.TypeDetailView.as_view(), name='typeDetail'),
  path('stat-sheets/<int:pk>', views.StatDetailView.as_view(), name='statDetail'),
]