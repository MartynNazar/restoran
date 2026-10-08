from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, WorkItem
from .forms import ContactRequestForm

def home_page(request):
    return render(request, 'home.html')





def home_view(request):
    success = False
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactRequestForm()
    else:
        form = ContactRequestForm()

    return render(request, 'restoran/home.html', {'form': form, 'success': success})


def services_view(request):
    query = request.GET.get('q', '').strip()
    selected_category_id = request.GET.get('category', '')

    works = WorkItem.objects.all().order_by('-id')

    if query:
        words = query.split()
        q_object = Q()
        for word in words:
            q_object |= Q(title__icontains=word) | Q(description__icontains=word)
        works = works.filter(q_object)

    if selected_category_id and selected_category_id.isdigit():
        works = works.filter(category_id=selected_category_id)

    paginator = Paginator(works, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'categories': categories,
        'page_obj': page_obj,
        'query': query,
        'selected_category_id': int(selected_category_id) if selected_category_id.isdigit() else '',
    }
    return render(request, 'services.html', context)


def autocomplete_ajax(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        works = WorkItem.objects.filter(title__icontains=query)[:5]
        results = [work.title for work in works]
    return JsonResponse(results, safe=False)


def contacts_view(request):
    return render(request, 'contacts.html')


def register_view(request):
    return render(request, 'register.html')


from django.shortcuts import render, redirect
from .forms import ContactRequestForm


def contact_view(request):
    success = False
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactRequestForm()
    else:
        form = ContactRequestForm()

    # Зверни увагу на назву шаблону тут:
    return render(request, 'contact.html', {'form': form, 'success': success})