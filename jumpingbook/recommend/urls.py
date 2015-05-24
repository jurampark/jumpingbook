from django.conf.urls import patterns, url
from feasible import views
from feasible.views import FacebookView
from recommend.views import BookListView
from supervisor.views import ScrapKyoboBookView

urlpatterns = patterns('',
   url(r'^book/', BookListView.as_view(), name='book_list'),
)