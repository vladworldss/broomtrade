from django.urls import re_path
from page import views

urlpatterns = [
    re_path(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name='index'),
    re_path(r'^good/(?P<good_id>\d+)/$', views.good, name="good")
]
