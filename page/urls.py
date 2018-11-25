from django.urls import re_path
from page import views
from page.twviews import GoodListView, GoodDetailView
from page.forms import GoodCreate, GoodUpdate, GoodDelete


urlpatterns = [
    # re_path(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name='index'),
    re_path(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name='index'),

    # re_path(r'^good/(?P<good_id>\d+)/$', views.good, name="good")
    re_path(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name="good"),
    re_path(r'^(?P<cat_id>\d+)/add/$', GoodCreate.as_view(), name='good_add'),
    re_path(r'^good/(?P<good_id>\d+)/edit/$', GoodUpdate.as_view(), name='good_edit'),
    re_path(r'^good/(?P<good_id>\d+)/delete/$', GoodDelete.as_view(), name='good_delete'),
]
