# coding: utf-8
from django.conf.urls import re_path
from main.views import MainPageView


urlpatterns = [re_path(r'^$', MainPageView.as_view(), name="main"),
               ]
