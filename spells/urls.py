from django.urls import path
from . import views

app_name = 'spells'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('spellCast/<int:pk>/', views.CastDetailView.as_view(), name='castDetail'),
  # REST API URLs
  path ('api/spell'                 , views.SpellViewSet.as_view({'get':'list'})),
  path ('api/spell/<int:pk>'        , views.SpellViewSet.as_view({'get':'retrieve'})),
  path ('api/spellcast'             , views.SpellCastViewSet.as_view({'get':'list'})),
  path ('api/spellcast/<int:pk>'    , views.SpellCastViewSet.as_view({'get':'retrieve'})),
  path ('api/learnedspell'          , views.LearnedSpellViewSet.as_view({'get':'list'})),
  path ('api/learnedspell/<int:pk>' , views.LearnedSpellViewSet.as_view({'get':'retrieve'})),
]