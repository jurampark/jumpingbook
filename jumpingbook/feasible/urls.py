from django.conf.urls import patterns, url
from feasible import views
from feasible.views import FacebookView

urlpatterns = patterns('',
   url(r'^facebook$', FacebookView.as_view(), name='facebook'),
)