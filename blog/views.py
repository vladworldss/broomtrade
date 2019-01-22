from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin
from django.db.models import Q

from blog.models import Blog
from generic.controllers import PageNumberView
from generic.mixins import CategoryListMixin, PageNumberMixin


class SearchMixin(ContextMixin):
    search = ""
    tag = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.search
        context["tag"] = self.tag
        return context


class BlogListView(PageNumberView, ArchiveIndexView, SearchMixin, CategoryListMixin):
    model = Blog
    date_field = "posted"
    template_name = "blog_index.html"
    paginate_by = 2
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        blog = super().get_queryset()
        if self.search:
            blog = blog.filter(Q(title__contains=self.search) |
                               Q(description__contains=self.search) |
                               Q(content__contains=self.search))
        if self.tag:
            blog = blog.filter(tags__name=self.tag)
        return blog


class BlogDetailView(PageNumberView, DetailView, SearchMixin, PageNumberMixin):
    model = Blog
    template_name = "blog.html"
