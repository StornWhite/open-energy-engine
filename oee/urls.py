from django.urls import re_path
from django.contrib import admin

from oee.views import hello_world


urlpatterns = [
    re_path(r"^admin/?", admin.site.urls),
    re_path(r".*", hello_world, name="Hello World")
]

