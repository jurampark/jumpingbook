from django.conf.urls import patterns, url
from main.views import IndexView

urlpatterns = patterns('',
   url(r'^$', IndexView.as_view(), name='main'),
)