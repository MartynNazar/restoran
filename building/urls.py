from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from restoran.views import home_page, services_page, gallery_page, contacts_page, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('services/', services_page, name='services'),
    path('gallery/', gallery_page, name='gallery'),
    path('contacts/', contacts_page, name='contacts'),
    path('register/', register_view, name='register'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)