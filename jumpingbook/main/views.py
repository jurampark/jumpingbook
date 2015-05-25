from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "main/login.html"

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "main/index.html"

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "main/mypage.html"