"""CritRoleDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,  path
from django.conf.urls import url

urlpatterns = [
    path('languages/', include('languages.urls')),
    path('damages/', include('damages.urls')),
    path('encounters/', include('encounters.urls')),
    path('spells/', include('spells.urls')),
    path('items/', include('items.urls')),
    path('players/',include ('players.urls')),
    path('campaigns/', include ('campaigns.urls')),
    path('classes/', include('classes.urls')),
    path('races/', include('races.urls')),
    path('characters/', include('characters.urls')),
    path('rolls/', include('rolls.urls')),
    path('episodes/', include('episodes.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]