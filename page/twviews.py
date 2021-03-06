from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, ProcessFormView
)
from django.urls import reverse
from django.contrib import messages, sessions
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from .models import Category, Good, BlogArticle
from .forms import GoodForm, CategoryForm, CategoryFormset, LoginForm


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
        goods = Good.objects.filter(category=self.cat).order_by('name')
        tags_name = self.request.GET.get('tag')
        if tags_name:
            goods = goods.filter(tags__name=tags_name)
        return goods


class GoodDetailView(DetailView, CategoryListMixin):
    template_name = 'good.html'
    model = Good
    pk_url_kwarg = 'good_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pn'] = self.request.GET.get('page', 1)
        return context


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
    form_class = GoodForm
    template_name = 'good_add.html'
    # fields = '__all__'

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


class _GoodCreate(TemplateView):
    form = None
    template_name = 'good_add.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.kwargs['cat_id'] is None:
                cat = Category.objects.first()
            else:
                cat = Category.objects.get(pk=self.kwargs['cat_id'])

            in_stock = request.session.get('in_stock', True)
            self.form = GoodForm(initial={'category': cat, 'in_stock': in_stock})
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login/?next=' + request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        cat = Category.objects.get(pk=self.kwargs['cat_id'])
        context['category'] = cat
        context['pn'] = self.request.GET.get('page', 1)
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['cat_id'] is None:
            cat = Category.objects.first()
        else:
            cat = Category.objects.get(pk=self.kwargs['cat_id'])
        self.form = GoodForm(request.POST, request.FILES)
        if self.form.is_valid():
            request.session['in_stock'] = self.form.cleaned_data['in_stock']
            self.form.save()
            messages.add_message(request, messages.SUCCESS, 'Товар успешно добавлен в список')
            return redirect('index',  cat_id=cat.id)
        else:
            return super().get(request, *args, **kwargs)


class GoodUpdate(UpdateView, GoodEditMixin, GoodEditView):
    model = Good
    form_class = GoodForm
    template_name = 'good_edit.html'
    pk_url_kwarg = 'good_id'

    def post(self, request, *args, **kwargs):
        cat_id = Good.objects.get(pk=kwargs['good_id']).category.id
        self.success_url = reverse("index", kwargs={'cat_id': cat_id})
        return super().post(request, *args, **kwargs)


class _GoodUpdate(TemplateView):
    form = None
    template_name = 'good_edit.html'

    def get(self, request, *args, **kwargs):
        self.form = GoodForm(instance=Good.objects.get(pk=self.kwargs['good_id']))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['good'] = Good.objects.get(pk=self.kwargs['good_id'])
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs['good_id'])
        self.form = GoodForm(request.POST, request.FILES, instance=good)
        if self.form.is_valid():
            self.form.save()
            return redirect('index', cat_id=good.category.id)
        else:
            return super().get(request, *args, **kwargs)


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


class CategoryListView(TemplateView):
    template_name = "cats.html"
    formset = None

    def get(self, request, *args, **kw):
        self.formset = CategoryFormset()
        return super().get(request, *args, **kw)

    def get_context_data(self, **kw):
        context = super().get_context_data(**kw)
        context["formset"] = self.formset
        return context

    def post(self, request, *args, **kw):
        self.formset = CategoryFormset(request.POST)
        if self.formset.is_valid():
            self.formset.save()
            #todo: сделать норм возврат
            return redirect("index")
        else:
            return super().get(request, *args, **kw)

# RAW View
class BlogUpdate(TemplateView):
    template_name = "cats.html"
    formset = None

    def get(self, request, *args, **kw):
        blog = BlogArticle.objects.get(pk=self.kwargs["blog_id"])
        if blog.user == request.user:
            # some formset logic
            pass
        else:
            return redirect("login")


class LoginView(TemplateView):
    form = None
    template_name = 'login.html'

    def get(self, request, *args, **kw):
        self.form = LoginForm()
        return super().get(request, *args, **kw)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kw):
        self.form = LoginForm(request.POST)
        if self.form.is_valid():
            user = authenticate(username=self.form.cleaned_data['username'],
                                password=self.form.cleaned_data['password']
                                )
            if user and user.is_active:
                login(request, user)
                return redirect('index')
        else:
            return super().get(request, *args, **kw)


class LogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, *args, **kw):
        logout(request)
        # return redirect('index')
        return super().get(request, *args, **kw)
