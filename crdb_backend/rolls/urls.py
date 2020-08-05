from django.urls import path
from . import views

app_name = 'rolls'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('types/', views.TypeListView.as_view(), name='typeIndex'),
  path('types/<int:pk>', views.TypeDetailView.as_view(), name='typeDetail'),
  #REST API URLs
  path('api/roll'                   , views.RollsViewSet.as_view({'get':'list'})),
  path('api/roll/<int:pk>'          , views.RollsViewSet.as_view({'get':'retrieve'})),
  path('api/rolltype'               , views.RollTypeViewSet.as_view({'get':'list'})),
  path('api/rolltype/<int:pk>'      , views.RollTypeViewSet.as_view({'get':'retrieve'})),
  path('api/advantage'              , views.AdvantageViewSet.as_view({'get':'list'})),
  path('api/advantage/<int:pk>'     , views.AdvantageViewSet.as_view({'get':'retrieve'})),
  path('api/advantagetype'          , views.AdvantageTypeViewSet.as_view({'get':'list'})),
  path('api/advantagetype/<int:pk>' , views.AdvantageTypeViewSet.as_view({'get':'retrieve'})),
  path('api/kill'                   , views.KillViewSet.as_view({'get':'list'})),
  path('api/kill/<int:pk>'          , views.KillViewSet.as_view({'get':'retrieve'})),
  path('api/die'                    , views.DieViewSet.as_view({'get':'list'})),
  path('api/die/<int:pk>'           , views.DieViewSet.as_view({'get':'retrieve'})),
]