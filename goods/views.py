from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.contrib import messages
from django.forms.models import inlineformset_factory

from categories.models import Category
from goods.models import Good, GoodImage
from goods.forms import GoodForm
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView

# logger = logging.getLogger(__name__)

GoodImagesFormset = inlineformset_factory(Good, GoodImage, can_order=True, fields='__all__')


class SortMixin(ContextMixin):
  sort = "0"
  order = "A"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["sort"] = self.sort
    context["order"] = self.order
    return context

  def make_full_url(self, reverse_url):
      return '{}?page={}&sort={}&order={}'.format(reverse_url,
                                                  self.request.GET["page"],
                                                  self.request.GET["sort"],
                                                  self.request.GET["order"]
                                                  )


class GoodsListView(PageNumberView, ListView, SortMixin, CategoryListMixin):
  model = Good
  template_name = "goods_index.html"
  paginate_by = 2
  cat = None

  def get(self, request, *args, **kwargs):
    if self.kwargs["pk"] == None:
        self.cat = Category.objects.first()
    else:
        self.cat = Category.objects.get(pk=self.kwargs["pk"])
    return super().get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["category"] = self.cat
    return context

  def get_queryset(self):
    goods = Good.objects.filter(category=self.cat)
    if self.sort == "2":
        if self.order == "D":
            goods = goods.order_by("-in_stock", "name")
        else:
            goods = goods.order_by("in_stock", "name")
    elif self.sort == "1":
        if self.order == "D":
            goods = goods.order_by("-price", "name")
        else:
            goods = goods.order_by("price", "name")
    else:
        if self.order == "D":
            goods = goods.order_by("-name")
        else:
            goods = goods.order_by("name")
    return goods


class GoodDetailView(PageNumberView, DetailView, SortMixin, PageNumberMixin):
    model = Good
    template_name = "good.html"


class GoodCreate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    template_name = "good_add.html"
    cat = None
    form = None
    formset = None
    __success_msg = "Товар успешно добавлен"

    def get(self, request, *args, **kwargs):
        if self.kwargs["pk"] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk = self.kwargs["pk"])
        self.form = GoodForm(initial={"category": self.cat})
        self.formset = GoodImagesFormset()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.cat
        context["form"] = self.form
        context["formset"] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.form = GoodForm(request.POST, request.FILES)
        if self.form.is_valid():
            new_good = self.form.save()
            self.formset = GoodImagesFormset(request.POST, request.FILES, instance = new_good)
            if self.formset.is_valid():
                self.formset.save()
                messages.add_message(request, messages.SUCCESS, self.__success_msg)
                reverse_link = reverse("goods_index", kwargs={"pk": new_good.category.pk})
                return redirect(self.make_full_url(reverse_link))
        if self.kwargs["pk"] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs["pk"])
        self.formset = GoodImagesFormset(request.POST, request.FILES)
        return super().get(request, *args, **kwargs)


class GoodUpdate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    good = None
    template_name = "good_edit.html"
    form = None
    formset = None
    __success_msg = "Товар успешно изменен"

    def get(self, request, *args, **kwargs):
        self.good = Good.objects.get(pk = self.kwargs["pk"])
        self.form = GoodForm(instance = self.good)
        self.formset = GoodImagesFormset(instance=self.good)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["good"] = self.good
        context["form"] = self.form
        context["formset"] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(request.POST, request.FILES, instance = self.good)
        self.formset = GoodImagesFormset(request.POST, request.FILES, instance=self.good)
        if self.form.is_valid():
            self.form.save()
            if self.formset.is_valid():
                self.formset.save()
                messages.add_message(request, messages.SUCCESS, self.__success_msg)
                reverse_link = reverse("goods_index", kwargs={"pk": self.good.category.pk})
                return redirect(self.make_full_url(reverse_link))
        return super().get(request, *args, **kwargs)


class GoodDelete(PageNumberView, DeleteView, SortMixin, PageNumberMixin):
    model = Good
    template_name = "good_delete.html"
    __success_msg = "Товар успешно удален"

    def post(self, request, *args, **kwargs):
        reverse_link = reverse("goods_index", kwargs={"pk": Good.objects.get(pk = kwargs["pk"]).category.pk})
        self.success_url = self.make_full_url(reverse_link)
        messages.add_message(request, messages.SUCCESS, self.__success_msg)
        return super().post(request, *args, **kwargs)
