from django.shortcuts import render

def home_page(request):
    return render(request, 'index.html')

def services_page(request):
    return render(request, 'services.html')

def gallery_page(request):
    return render(request, 'gallery.html')

def contacts_page(request):
    return render(request, 'contacts.html')