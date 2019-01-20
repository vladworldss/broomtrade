# coding: utf-8
from django.views.generic.base import ContextMixin
from categories.models import Category


class CategoryListMixin(ContextMixin):

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["current_url"] = self.request.path
    context["categories"] = Category.objects.all()
    return context


class PageNumberMixin(CategoryListMixin):

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["pn"] = self.request.GET.get("page", "1")
    return context
