from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Category, Good


class CategoryListMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.order_by('name')
        return context


class GoodListView(ListView, CategoryListMixin):
    template_name = 'index.html'
    queryset = Good.objects.order_by('name')
    paginate_by = 1
    cat = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['cat_id'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['cat_id'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.cat
        return context

    def get_queryset(self):
        # вызывается позже, чем get_context_data --> self.cat уже будет
        return Good.objects.filter(category=self.cat).order_by('name')


class GoodDetailView(DetailView, CategoryListMixin):
    template_name = 'good.html'
    model = Good
    pk_url_kwarg = 'good_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pn'] = self.request.GET.get('page', 1)
        return context
