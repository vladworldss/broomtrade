from django.views.generic.base import TemplateView
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.views.generic.list import ListView
from .models import Category, Good


class GoodListView(ListView):
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
        context['cats'] = Category.objects.order_by('name')
        context['category'] = self.cat
        return context

    def get_queryset(self):
        # вызывается позже, чем get_context_data --> self.cat уже будет
        return Good.objects.filter(category=self.cat).order_by('name')


class GoodDetailView(TemplateView):
    template_name = 'good.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pn'] = self.request.GET.get('page', 1)
        context['cats'] = Category.objects.order_by('name')
        try:
            context['good'] = Good.objects.get(pk=kwargs['good_id'])
        except Good.DoesNotExist:
            raise Http404
        return context
