from django.urls import path
from . import views

app_name = 'encounters'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  # REST API URLs
  path ('api/encounter', views.CombatEncounterList.as_view()),
  path ('api/encounter/<int:pk>', views.CombatEncounterDetail.as_view()),
  path ('api/combatapperance', views.CombatApperanceList.as_view()),
  path ('api/combatapperance/<int:pk>', views.CombatApperanceDetail.as_view()),
  path ('api/initiativeorder', views.InitiativeOrderList.as_view()),
  path ('api/initiativeorder/<int:pk>', views.InitiativeOrderDetail.as_view()),
]