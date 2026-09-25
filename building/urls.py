from django.contrib import admin
from django.urls import path
from restoran.views import home_page, services_page, gallery_page, contacts_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('services/', services_page, name='services'),
    path('gallery/', gallery_page, name='gallery'),
    path('contacts/', contacts_page, name='contacts'),
]