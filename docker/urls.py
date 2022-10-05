from .base_urls import *
from django.urls import re_path, include

urlpatterns += [
    re_path(r'^', include('pathways.urls')),
    re_path(r'^support', include('userservice.urls')),
    re_path(r'^persistent_message/', include('persistent_message.urls')),
]
