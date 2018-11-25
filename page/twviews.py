from django.views.generic.base import TemplateView
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from .models import Category, Good


class GoodListView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.request.GET.get('page', 1)
        context['cats'] = Category.objects.order_by('name')
        if kwargs['cat_id'] is None:
            context['category'] = Category.objects.first()
        else:
            context['category'] = Category.objects.get(pk=kwargs['cat_id'])

        _goods = Good.objects.filter(category=context['category']).order_by('name')
        pag = Paginator(_goods, 1)
        try:
            context['goods'] = pag.page(page_num)
        except InvalidPage:
            context['goods'] = pag.page(1)
        return context


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
