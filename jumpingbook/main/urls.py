from django.conf.urls import patterns, url
from main.views import IndexView, LoginView, MyPageView, BookRatingView, BookRecommendedView, BookSearchView, \
    AddFriendView, BookDetailView, BookCommentView

urlpatterns = patterns('',
   url(r'^$', IndexView.as_view(), name='index'),
   url(r'^login/$', LoginView.as_view(), name='login'),
   url(r'^mypage/$', MyPageView.as_view(), name='mypage'),
   url(r'^book/rating$', BookRatingView.as_view(), name='book_rating'),
   url(r'^book/recommended$', BookRecommendedView.as_view(), name='book_recommended'),
   url(r'^book/search$', BookSearchView.as_view(), name='book_search'),
   url(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
   url(r'^book/(?P<pk>\d+)/comment$', BookCommentView.as_view(), name='book_comment'),
   url(r'^friend/add$', AddFriendView.as_view(), name='add_friend')
)
