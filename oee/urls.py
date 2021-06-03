from django.urls import re_path, include
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from oee.views import hello_world


schema_view = get_schema_view(
    openapi.Info(
        title="Open Energy Engine",
        default_version='v1',
        description="A storage and computation engine for energy data.",
        contact=openapi.Contact(email="storn@open-energy-engine.org")
    ),
    public=False,
    # Todo: evaluate permission classes and authentication
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r"^admin/?", admin.site.urls),
    re_path(r"^auth/?", include('rest_auth.urls')),
    re_path(r'^auth/registration/', include('rest_auth.registration.urls')),
    re_path(r"^hello/?", hello_world, name="Hello World"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r"^$", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
