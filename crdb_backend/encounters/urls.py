from django.urls import path
from . import views

app_name = 'encounters'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  # REST API URLs
  path ('api/encounter'                , views.CombatEncounterViewSet.as_view({'get':'list'})),
  path ('api/encounter/<int:pk>'       , views.CombatEncounterViewSet.as_view({'get':'retrieve'})),
  path ('api/combatapperance'          , views.CombatApperanceViewSet.as_view({'get':'list'})),
  path ('api/combatapperance/<int:pk>' , views.CombatApperanceViewSet.as_view({'get':'retrieve'})),
  path ('api/initiativeorder'          , views.InitiativeOrderViewSet.as_view({'get':'list'})),
  path ('api/initiativeorder/<int:pk>' , views.InitiativeOrderViewSet.as_view({'get':'retrieve'})),
]