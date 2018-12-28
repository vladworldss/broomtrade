from django.conf.urls import re_path
from django.contrib.auth.decorators import login_required

from imagepool.views import get_list, upload_file, delete_file

urlpatterns = [
    re_path(r'^$', login_required(get_list), name="imagepool_index"),
    re_path(r'^upload/$', login_required(upload_file), name="imagepool_upload"),
    re_path(r'^(?P<pk>\d+)/delete/$', login_required(delete_file), name="imagepool_delete"),
]
