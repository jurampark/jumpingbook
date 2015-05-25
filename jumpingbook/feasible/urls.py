from django.conf.urls import patterns, url
from feasible import views
from feasible.views import FacebookView, MypageView, ShopView

urlpatterns = patterns('',
   url(r'^facebook$', FacebookView.as_view(), name='facebook'),
   url(r'^mypage$', MypageView.as_view(), name='mypage'),
   url(r'^shop$', ShopView.as_view(), name='shop'),
)