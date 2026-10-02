from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from restoran.views import (
    home_page,
    services_view,
    contacts_view,
    register_view,
    autocomplete_ajax
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('services/', services_view, name='services'),
    path('contacts/', contacts_view, name='contacts'),
    path('register/', register_view, name='register'),
    path('autocomplete/', autocomplete_ajax, name='autocomplete_ajax'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)