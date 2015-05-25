from django.views.generic import TemplateView


class FacebookView(TemplateView):
    template_name = "feasible/facebook.html"

class MypageView(TemplateView):
    template_name = "feasible/mypage.html"

class ShopView(TemplateView):
    template_name = "feasible/shop.html"