from django.urls import path

from . import views

app_name = 'episodes'
urlpatterns = [
    path('view/', views.IndexView.as_view(), name='index'),
    path('view/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('view/apperances/', views.ApperanceIndexView.as_view(), name='apperanceIndex'),
    path('view/apperances/<int:pk>', views.ApperanceDetailView.as_view(), name='apperanceDetail'),
    # REST API URLs
    path('', views.EpisodeViewSet.as_view({'get': 'list'})),
    path('<int:pk>', views.EpisodeViewSet.as_view({'get': 'retrieve'})),
    path('apperance', views.ApperanceViewSet.as_view({'get': 'list'})),
    path('apperance/<int:pk>', views.ApperanceViewSet.as_view({'get': 'retrieve'})),
    path('attendance', views.AttendanceViewSet.as_view({'get': 'list'})),
    path('attendance/<int:pk>', views.AttendanceViewSet.as_view({'get': 'retrieve'})),
    path('attendancetype', views.AttendanceTypeViewSet.as_view({'get': 'list'})),
    path('attendancetype/<int:pk>', views.AttendanceTypeViewSet.as_view({'get': 'retrieve'})),
    path('levelprog', views.AttendanceViewSet.as_view({'get': 'list'})),
    path('levelprog/<int:pk>', views.AttendanceViewSet.as_view({'get': 'retrieve'})),
    path('live', views.LiveViewSet.as_view({'get': 'list'})),
    path('live/<int:pk>', views.LiveViewSet.as_view({'get': 'retrieve'})),
    path('vodtype', views.VodTypeViewSet.as_view({'get': 'list'})),
    path('vodtype/<int:pk>', views.VodTypeViewSet.as_view({'get': 'retrieve'})),
    path('vodlinks', views.VodLinksViewSet.as_view({'get': 'list'})),
    path('vodlinks/<int:pk>', views.VodLinksViewSet.as_view({'get': 'retrieve'})),
]
