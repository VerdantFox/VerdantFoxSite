# from django.http import request
from django.views.generic import TemplateView
# from django.contrib.messages import get_messages


class HomePage(TemplateView):
    template_name = 'index.html'


