from django.conf.urls import patterns, url
from main.views import IndexView, LoginView, MyPageView

urlpatterns = patterns('',
   url(r'^$', IndexView.as_view(), name='index'),
   url(r'^login/$', LoginView.as_view(), name='login'),
   url(r'^mypage/$', MyPageView.as_view(), name='mypage'),
)