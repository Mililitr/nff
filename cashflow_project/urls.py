"""
Конфигурация URL-маршрутов проекта Django для веб-сервиса управления движением денежных средств.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cashflow.urls')),  # Включаем URL-маршруты приложения cashflow
]

# Добавляем маршруты для статических и медиа-файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)