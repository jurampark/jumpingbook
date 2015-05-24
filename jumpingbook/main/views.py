from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "main/login.html"

class IndexView(TemplateView):
    template_name = "main/index.html"

    #optional
    # login_url = reverse_lazy("main:login")
    # redirect_field_name = "next"
    # raise_exception = True