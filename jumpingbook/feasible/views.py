from django.views.generic import TemplateView


class FacebookView(TemplateView):
    template_name = "feasible/facebook.html"