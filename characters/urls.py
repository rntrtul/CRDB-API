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
  path ('api/ability'               , views.AbilityList.as_view()),
  path ('api/ability/<int:pk>'      , views.AbilityDetail.as_view()),
  path ('api/abilityscore'          , views.AbilityScoreList.as_view()),
  path ('api/abilityscore/<int:pk>' , views.AbilityScoreDetail.as_view()),
  path ('api/alignment'             , views.AlignmentList.as_view()),
  path ('api/alignment/<int:pk>'    , views.AlignmentDetail.as_view()),
  path ('api/character'             , views.CharacterList.as_view()),
  path ('api/character/<int:pk>'    , views.CharacterDetail.as_view()),
  path ('api/charactertype'         , views.CharacterTypeList.as_view()),
  path ('api/charactertype/<int:pk>', views.CharacterTypeDetail.as_view()),
  path ('api/classtaken'            , views.ClassTakenList.as_view()),
  path ('api/classtaken/<int:pk>'   , views.ClassTakenDetail.as_view()),
  path ('api/savingthrows'          , views.SavingThrowList.as_view()),
  path ('api/savingthrows/<int:pk>' , views.SavingThrowDetail.as_view()),
  path ('api/skill'                 , views.SkillsList.as_view()),
  path ('api/skill/<int:pk>'        , views.SkillsDetail.as_view()),
  path ('api/skilllist'             , views.SkillListList.as_view()),
  path ('api/skilllist/<int:pk>'    , views.SkillListDetail.as_view()),
  path ('api/statsheet'             , views.StatSheetList.as_view()),
  path ('api/statsheet/<int:pk>'    , views.StatSheetDetail.as_view()),
]