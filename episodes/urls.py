from django.urls import path
from . import views

app_name = 'episodes'
urlpatterns = [
  path ('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('apperances/', views.ApperanceIndexView.as_view(), name='apperanceIndex'),
  path('apperances/<int:pk>', views.ApperanceDetailView.as_view(), name='apperanceDetail'),
  #REST API URLs
  path('api/episode'                 , views.EpisodeViewSet.as_view({'get':'list'}) ),
  path('api/episode/<int:pk>'        , views.EpisodeViewSet.as_view({'get':'retrieve'})),
  path('api/apperance'               , views.ApperanceViewSet.as_view({'get':'list'}) ),
  path('api/apperance/<int:pk>'      , views.ApperanceViewSet.as_view({'get':'retrieve'}) ),
  path('api/attendance'              , views.AttendanceViewSet.as_view({'get':'list'}) ),
  path('api/attendance/<int:pk>'     , views.AttendanceViewSet.as_view({'get':'retrieve'}) ),
  path('api/attendancetype'          , views.AttendanceTypeViewSet.as_view({'get':'list'}) ),
  path('api/attendancetype/<int:pk>' , views.AttendanceTypeViewSet.as_view({'get':'retrieve'}) ),
  path('api/levelprog'               , views.AttendanceViewSet.as_view({'get':'list'}) ),
  path('api/levelprog/<int:pk>'      , views.AttendanceViewSet.as_view({'get':'retrieve'}) ),
  path('api/live'                    , views.LiveViewSet.as_view({'get':'list'})),
  path('api/live/<int:pk>'           , views.LiveViewSet.as_view({'get':'retrieve'})),
  path('api/vodtype'                 , views.VodTypeViewSet.as_view({'get':'list'})),
  path('api/vodtype/<int:pk>'        , views.VodTypeViewSet.as_view({'get':'retrieve'})),
  path('api/vodlinks'                , views.VodLinksViewSet.as_view({'get':'list'})),
  path('api/vodlinks/<int:pk>'       , views.VodLinksViewSet.as_view({'get':'retrieve'})),
]