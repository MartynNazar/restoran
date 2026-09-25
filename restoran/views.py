from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Category, WorkItem

def home_page(request):
    return render(request, 'index.html')

def services_page(request):
    # Витягуємо всі категорії та роботи з бази даних для показу на сайті!
    categories = Category.objects.all()
    works = WorkItem.objects.all()
    context = {
        'categories': categories,
        'works': works,
    }
    return render(request, 'services.html', context)

def gallery_page(request):
    return render(request, 'gallery.html')

def contacts_page(request):
    return render(request, 'contacts.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматичний вхід після реєстрації
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', context={'form': form})