from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin


class MainPageView(TemplateView, CategoryListMixin):
  template_name = "mainpage.html"
