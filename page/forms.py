from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, ProcessFormView
)
from django.urls import reverse
from .models import Category, Good
from .twviews import CategoryListMixin


class GoodEditMixin(CategoryListMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pn'] = self.request.GET.get('page', 1)
        return context


class GoodEditView(ProcessFormView):

    def post(self, request, *args, **kwargs):
        pn = request.GET.get('page', 1)
        self.success_url = self.success_url + '?page=' + pn
        return super().post(request, *args, **kwargs)


class GoodCreate(CreateView, GoodEditMixin):
    model = Good
    template_name = 'good_add.html'
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        self.initial['category'] = Category.objects.get(pk=self.kwargs['cat_id'])
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        cat_id = Category.objects.get(pk=self.kwargs['cat_id']).id
        self.success_url = reverse('index', kwargs={'cat_id': cat_id})
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['cat_id'])
        return context


class GoodUpdate(UpdateView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = 'good_edit.html'
    pk_url_kwarg = 'good_id'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        cat_id = Good.objects.get(pk=kwargs['good_id']).category.id
        self.success_url = reverse("index", kwargs={'cat_id': cat_id})
        return super().post(request, *args, **kwargs)


class GoodDelete(DeleteView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = 'good_delete.html'
    pk_url_kwarg = 'good_id'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        cat_id = Good.objects.get(pk=kwargs['good_id']).category.id
        self.success_url = reverse('index', kwargs={'cat_id': cat_id})
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['good'] = Good.objects.get(pk=self.kwargs['good_id'])
        return context
