from django.conf.urls import re_path
from django.contrib.auth.decorators import login_required

from categories.views import CategoriesEdit

urlpatterns = [
    re_path(r'^$', login_required(CategoriesEdit.as_view()), name="categories_edit"),
]
