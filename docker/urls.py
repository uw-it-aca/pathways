from .base_urls import *
from django.conf.urls import include
from django.urls import re_path

urlpatterns += [
    re_path(r'^', include('pathways.urls')),
    re_path(r'^support/', include('persistent_message.urls')),
]
