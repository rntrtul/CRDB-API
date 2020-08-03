from django.urls import path
from . import views

app_name = 'languages'
urlpatterns = [
  # REST API URLs
  path ('api/language', views.LanguageList.as_view()),
  path ('api/language/<int:pk>', views.LanguageDetail.as_view()),
  path ('api/learnedlanaguage', views.LearnedLanguageList.as_view()),
  path ('api/learnedlanaguage/<int:pk>', views.LearnedLanguageDetail.as_view()),
]