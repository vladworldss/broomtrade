from django.urls import re_path
from django.contrib.auth.decorators import permission_required

from blog.views import BlogListView, BlogDetailView, BlogCreate, BlogUpdate, BlogDelete

urlpatterns = [
    re_path(r'^$', BlogListView.as_view(), name = "blog_index"),
    re_path(r'^(?P<pk>\d+)/detail/$', BlogDetailView.as_view(), name="blog_detail"),
    re_path(r'^add/$', permission_required("blog.add_blog")(BlogCreate.as_view()), name="blog_add"),
    re_path(r'^(?P<pk>\d+)/edit/$', permission_required("blog.change_blog")(BlogUpdate.as_view()), name="blog_edit"),
    re_path(r'^(?P<pk>\d+)/delete/$', permission_required("blog.delete_blog")(BlogDelete.as_view()), name="blog_delete"),
]
