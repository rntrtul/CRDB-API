from django.urls import path
from . import views

app_name = 'spells'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('spellCast/<int:pk>/', views.CastDetailView.as_view(), name='castDetail'),
  # REST API URLs
  path ('api/spell', views.SpellList.as_view()),
  path ('api/spellcast', views.SpellCastList.as_view()),
  path ('api/learnedspell', views.LearnedSpellList.as_view()),
  path ('api/spell/<int:pk>', views.SpellDetail.as_view()),
  path ('api/spellcast/<int:pk>', views.SpellCastDetail.as_view()),
  path ('api/learnedspell/<int:pk>', views.LearnedSpellDetail.as_view()),
]