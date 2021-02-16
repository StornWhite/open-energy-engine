from django.urls import re_path, include
from django.contrib import admin

from rest_auth import urls as rest_auth_urls

from oee.views import hello_world


urlpatterns = [
    re_path(r"^admin/?", admin.site.urls),
    re_path(r"^auth/", include(rest_auth_urls)),
    re_path(r".*", hello_world, name="Hello World")
]
