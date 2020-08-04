from django.urls import path
from . import views

app_name = 'languages'
urlpatterns = [
  # REST API URLs
  path ('api/language'                  , views.LanguageViewSet.as_view({'get':'list'})),
  path ('api/language/<int:pk>'         , views.LanguageViewSet.as_view({'get':'retrieve'})),
  path ('api/learnedlanaguage'          , views.LearnedLanguageViewSet.as_view({'get':'list'})),
  path ('api/learnedlanaguage/<int:pk>' , views.LearnedLanguageViewSet.as_view({'get':'retrieve'})),
]