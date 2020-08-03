from django.urls import path
from . import views

app_name = 'rolls'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('types/', views.TypeListView.as_view(), name='typeIndex'),
  path('types/<int:pk>', views.TypeDetailView.as_view(), name='typeDetail'),
  #REST API URLs
  path('api/roll', views.RollsList.as_view()),
  path('api/roll/<int:pk>', views.RollsDetail.as_view()),
  path('api/rolltype', views.RollTypeList.as_view()),
  path('api/rolltype/<int:pk>', views.RollTypeDetail.as_view()),
  path('api/advantage', views.AdvantageList.as_view()),
  path('api/advantage/<int:pk>', views.AdvantageDetail.as_view()),
  path('api/advantagetype', views.AdvantageTypeList.as_view()),
  path('api/advantagetype/<int:pk>', views.AdvantageTypeDetail.as_view()),
  path('api/kill', views.KillList.as_view()),
  path('api/kill/<int:pk>', views.KillDetail.as_view()),
  path('api/die', views.DieList.as_view()),
  path('api/die/<int:pk>', views.DieDetail.as_view()),
]