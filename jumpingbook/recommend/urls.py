from django.conf.urls import patterns, url
from feasible import views
from feasible.views import FacebookView
from recommend.views import BookListView, RatingBookView, RatedBookListView
from supervisor.views import ScrapKyoboBookView

urlpatterns = patterns('',
   url(r'^book/$', BookListView.as_view(), name='book_list'),
   url(r'^rating/book/$', RatingBookView.as_view(), name='book_rating'),
   url(r'^book/rated/$', RatedBookListView.as_view(), name='rated_book'),
   url(r'^rating/book/cancel$', CancelRatingBookView.as_view(), name='cancel_rating'),

)
