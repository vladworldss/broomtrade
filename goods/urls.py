from django.conf.urls import re_path
from django.contrib.auth.decorators import permission_required

from goods.views import (
    GoodsListView, GoodDetailView, GoodCreate, GoodUpdate, GoodDelete, RssGoodsListFeed, AtomGoodsListFeed
)

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', GoodsListView.as_view(), name="goods_index"),
    re_path(r'^(?P<pk>\d+)/detail/$', GoodDetailView.as_view(), name="goods_detail"),
    re_path(r'^(?P<pk>\d+)/add/$', permission_required("goods.add_good")(GoodCreate.as_view()), name="goods_add"),
    re_path(r'^(?P<pk>\d+)/edit/$', permission_required("goods.change_good")(GoodUpdate.as_view()), name="goods_edit"),
    re_path(r'^(?P<pk>\d+)/delete/$', permission_required("goods.delete_good")(GoodDelete.as_view()), name="goods_delete"),
    re_path(r'^(?P<pk>\d+)/feed/rss/$', RssGoodsListFeed(), name="goods_feed_rss"),
    re_path(r'^(?P<pk>\d+)/feed/atom/$', AtomGoodsListFeed(), name="goods_feed_atom"),
]
