from django.urls import path
from . import views

app_name = 'episodes'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('apperances/', views.ApperanceIndexView.as_view(), name='apperanceIndex'),
  path('apperances/<int:pk>', views.ApperanceDetailView.as_view(), name='apperanceDetail'),
  #REST API URLs
  path('api/episode', views.EpisodeList.as_view() ),
  path('api/episode/<int:pk>', views.EpisodeDetail.as_view()),
  path('api/apperance', views.ApperanceList.as_view() ),
  path('api/apperance/<int:pk>', views.ApperanceDetail.as_view() ),
  path('api/attendance', views.AttendanceList.as_view() ),
  path('api/attendance/<int:pk>', views.AttendanceDetail.as_view() ),
  path('api/attendancetype', views.AttendanceTypeList.as_view() ),
  path('api/attendancetype/<int:pk>', views.AttendanceTypeDetail.as_view() ),
  path('api/levelprog', views.AttendanceList.as_view() ),
  path('api/levelprog/<int:pk>', views.AttendanceDetail.as_view() ),
  path('api/live', views.LiveList.as_view()),
  path('api/live/<int:pk>', views.LiveDetail.as_view()),
  path('api/vodtype', views.VodTypeList.as_view()),
  path('api/vodtype/<int:pk>', views.VodTypeDetail.as_view()),
  path('api/vodlinks', views.VodLinksList.as_view()),
  path('api/vodlinks/<int:pk>', views.VodLinksDetail.as_view()),
]