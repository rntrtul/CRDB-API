from django.urls import path
from . import views

app_name = 'characters'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('types/', views.TypeListView.as_view(), name='typeIndex'),
  path('types/<int:pk>', views.TypeDetailView.as_view(), name='typeDetail'),
  path('stat-sheets/<int:pk>', views.StatDetailView.as_view(), name='statDetail'),
  # REST API URLs
  path ('api/ability'               , views.AbilityViewSet.as_view({'get':'list'})),
  path ('api/ability/<int:pk>'      , views.AbilityViewSet.as_view({'get':'retrieve'})),
  path ('api/abilityscore'          , views.AbilityScoreViewSet.as_view({'get':'list'})),
  path ('api/abilityscore/<int:pk>' , views.AbilityScoreViewSet.as_view({'get':'retrieve'})),
  path ('api/alignment'             , views.AlignmentViewSet.as_view({'get':'list'})),
  path ('api/alignment/<int:pk>'    , views.AlignmentViewSet.as_view({'get':'retrieve'})),
  path ('api/character'             , views.CharacterViewSet.as_view({'get':'list'})),
  path ('api/character/<int:pk>'    , views.CharacterViewSet.as_view({'get':'retrieve'})),
  path ('api/charactertype'         , views.CharacterTypeViewSet.as_view({'get':'list'})),
  path ('api/charactertype/<int:pk>', views.CharacterTypeViewSet.as_view({'get':'retrieve'})),
  path ('api/classtaken'            , views.ClassTakenViewSet.as_view({'get':'list'})),
  path ('api/classtaken/<int:pk>'   , views.ClassTakenViewSet.as_view({'get':'retrieve'})),
  path ('api/savingthrows'          , views.SavingThrowViewSet.as_view({'get':'list'})),
  path ('api/savingthrows/<int:pk>' , views.SavingThrowViewSet.as_view({'get':'retrieve'})),
  path ('api/skill'                 , views.SkillViewSet.as_view({'get':'list'})),
  path ('api/skill/<int:pk>'        , views.SkillViewSet.as_view({'get':'retrieve'})),
  path ('api/skilllist'             , views.SkillListViewSet.as_view({'get':'list'})),
  path ('api/skilllist/<int:pk>'    , views.SkillListViewSet.as_view({'get':'retrieve'})),
  path ('api/statsheet'             , views.StatSheetViewSet.as_view({'get':'list'})),
  path ('api/statsheet/<int:pk>'    , views.StatSheetViewSet.as_view({'get':'retrieve'})),
]