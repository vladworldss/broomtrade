from django.urls import re_path
from page import views
from page import twviews

urlpatterns = [
    # re_path(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name='index'),
    re_path(r'^(?:(?P<cat_id>\d+)/)?$', twviews.GoodListView.as_view(), name='index'),

    # re_path(r'^good/(?P<good_id>\d+)/$', views.good, name="good")
    re_path(r'^good/(?P<good_id>\d+)/$', twviews.GoodDetailView.as_view(), name="good")
]
