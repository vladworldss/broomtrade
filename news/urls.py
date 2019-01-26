from django.conf.urls import re_path
from django.contrib.auth.decorators import permission_required

from news.views import(
    NewsListView, NewDetailView, NewCreate, NewUpdate, NewDelete,
    RssNewsListFeed, AtomNewsListFeed
)

urlpatterns = [
    re_path(r'^$', NewsListView.as_view(), name="news_index"),
    re_path(r'^(?P<pk>\d+)/$', NewDetailView.as_view(), name="news_detail"),
    re_path(r'^add/$', permission_required("news.add_new")(NewCreate.as_view()), name="news_add"),
    re_path(r'^(?P<pk>\d+)/edit/$', permission_required("news.change_new")(NewUpdate.as_view()), name="news_edit"),
    re_path(r'^(?P<pk>\d+)/delete/$', permission_required("news.delete_new")(NewDelete.as_view()), name="news_delete"),
    re_path(r'^feed/rss/$', RssNewsListFeed(), name="news_feed_rss"),
    re_path(r'^feed/atom/$', AtomNewsListFeed(), name="news_feed_atom"),
]
