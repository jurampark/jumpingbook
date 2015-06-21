from users.views import AddBookToBlackListView, AddBookToWishListView

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

urlpatterns = patterns('',
   url(r'^book/black/$', AddBookToBlackListView.as_view(), name='add_book_to_black_list'),
   url(r'^book/wish$', AddBookToWishListView.as_view(), name='add_book_to_wish_list'),
)