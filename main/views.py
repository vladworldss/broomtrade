from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from news.models import New


class MainPageView(TemplateView, CategoryListMixin):
  template_name = "mainpage.html"
  news = New.objects.all()[:5]

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['news'] = self.news
    return context
