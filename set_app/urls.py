"""
URL configuration for set_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from drf_spectacular.generators import SchemaGenerator

# --- Генераторы схем для mobile и website API --- #
class MobileSchemaGenerator(SchemaGenerator):
    def get_endpoints(self, request=None):
        endpoints = super().get_endpoints(request)
        return {
            path: data for path, data in endpoints.items() if path.startswith('/api/mobile')
        }

class WebSchemaGenerator(SchemaGenerator):
    def get_endpoints(self, request=None):
        endpoints = super().get_endpoints(request)
        return {
            path: data for path, data in endpoints.items() if path.startswith('/api/website')
        }


urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Основные API
    path('api/website/', include('set_main.urls', namespace='set_main')),
    path('api/mobile/', include('api_mobile.urls', namespace='api_mobile')),

    # Общая схема
    path('api/schema/v1/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/v1/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/v1/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Схема и документация только для website
    path('api/schema/website/', SpectacularAPIView.as_view(generator_class=WebSchemaGenerator), name='schema-website'),
    path('api/docs/website/', SpectacularSwaggerView.as_view(url_name='schema-website'), name='swagger-ui-website'),
    path('api/redoc/website/', SpectacularRedocView.as_view(url_name='schema-website'), name='redoc-website'),

    # Схема и документация только для mobile
    path('api/schema/mobile/', SpectacularAPIView.as_view(generator_class=MobileSchemaGenerator), name='schema-mobile'),
    path('api/docs/mobile/', SpectacularSwaggerView.as_view(url_name='schema-mobile'), name='swagger-ui-mobile'),
    path('api/redoc/mobile/', SpectacularRedocView.as_view(url_name='schema-mobile'), name='redoc-mobile'),
]

# Медиа и статика
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
