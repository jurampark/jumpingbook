from django.conf.urls import patterns, url
from feasible import views
from feasible.views import FacebookView
from supervisor.views import ScrapKyoboBookView

urlpatterns = patterns('',
   url(r'^scrap/kyobobook', ScrapKyoboBookView.as_view(), name='scrap_kyobo_book'),
)