from django.contrib import admin
from django.urls import path as _path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core.views import init_config_base_view
from public import errors



def path(pth, *args, **kwargs):
    return _path(f"{settings.NAME_POINT_API}/{pth}", *args, **kwargs)


urlpatterns = [
    path('', include('account.urls', namespace='account')),
    path('', include('task.urls', namespace='task')),
    path('', include('public.urls', namespace='public')),
    path('admin/', admin.site.urls),
]

# Drf-yasg - DOC
schema_view = get_schema_view(
    openapi.Info(
        title="Taski API",
        default_version=settings.API_VERSION,
        description="API Task manager Business",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(url="https://github.com/FZl47/Taski"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns.extend([
    # re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
])

# Serve media and static files in Develop
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Init Config Base View
init_config_base_view()


# Errors
handler404 = errors.error_404
