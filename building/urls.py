from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from restoran.views import (
    contact_view,
    home_page,
    services_view,
    contacts_view,
    autocomplete_ajax, gallery_view, calculator_view, register_view
)

urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_view, name='register'),
    path('services/', services_view, name='services'),
    path('services/', services_view, name='catalog'),  # Дублюємо name='catalog', щоб шаблон не видавав помилку
    path('contact/', contact_view, name='contact_us'),
    path('contacts/', contacts_view, name='contacts'),
    path('autocomplete/', autocomplete_ajax, name='autocomplete_ajax'),
    path('admin/', admin.site.urls),
    path('calculator/', calculator_view, name='calculator'),
    path('gallery/', gallery_view, name='gallery'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)