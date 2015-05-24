from django.conf.urls import patterns, url
from main.views import IndexView, LoginView

urlpatterns = patterns('',
   url(r'^$', IndexView.as_view(), name='index'),
   url(r'^login$', LoginView.as_view(), name='login'),
)