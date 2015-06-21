"""jumpingbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
import feasible

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls', namespace='main')),
    url(r'^feasible/', include('feasible.urls', namespace='feasible')),
    url(r'^supervisor/', include('supervisor.urls', namespace='supervisor')),
    url(r'^recommend/', include('recommend.urls', namespace='recommend')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
]
