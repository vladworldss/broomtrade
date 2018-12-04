from django.urls import re_path
from django.contrib.auth.decorators import login_required, permission_required
from page import views
from page.twviews import (GoodListView, GoodDetailView, GoodCreate,
                          GoodUpdate, GoodDelete, _GoodCreate, CategoryListView, _GoodUpdate
                          )

urlpatterns = [
    # re_path(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name='index'),
    re_path(r'^(?:(?P<cat_id>\d+)/)?$', login_required(GoodListView.as_view()), name='index'),

    # re_path(r'^good/(?P<good_id>\d+)/$', views.good, name="good")
    re_path(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name="good"),
    re_path(r'^(?P<cat_id>\d+)/add/$',
            permission_required("page.add_good")(_GoodCreate.as_view()),
            name='good_add'),

    re_path(r'^good/(?P<good_id>\d+)/edit/$',
            permission_required("page.change_good")(_GoodUpdate.as_view()),
            name='good_edit'),

    re_path(r'^good/(?P<good_id>\d+)/delete/$',
            permission_required("page.delete_good")(GoodDelete.as_view()),
            name='good_delete'),

    re_path(r'^cats/(?:(?P<cat_id>\d+)/)?$', CategoryListView.as_view(), name='categories'),
]
