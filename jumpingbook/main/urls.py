from django.conf.urls import patterns, url
from main.views import IndexView, LoginView, MyPageView, BookRatingView, BookRecommendedView, BookSearchView, \
    AddFriendView

urlpatterns = patterns('',
   url(r'^$', IndexView.as_view(), name='index'),
   url(r'^login/$', LoginView.as_view(), name='login'),
   url(r'^mypage/$', MyPageView.as_view(), name='mypage'),
   url(r'^book/rating$', BookRatingView.as_view(), name='book_rating'),
   url(r'^book/recommended$', BookRecommendedView.as_view(), name='book_recommended'),
   url(r'^book/search$', BookSearchView.as_view(), name='book_search'),
   url(r'^friend/add$', AddFriendView.as_view(), name='add_friend')
)
