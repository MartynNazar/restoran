import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Service, Category, Review, GalleryItem

# Твої дані для Telegram-бота
TELEGRAM_TOKEN = "9171871903:AAFwMf2YgpgZYo5us-p-36SMgO_Zm3J7mD0"
ADMIN_CHAT_ID = "1988776608"


def send_telegram_notification(text):
    """Функція для миттєвої відправки будь-яких подій з сайту в твій Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Помилка відправки в Telegram: {e}")


# --- ГОЛОВНА СТОРІНКА ---
def home_view(request):
    return render(request, 'home.html')


# --- КАТАЛОГ ПОСЛУГ ---
def services_view(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q')

    services_list = Service.objects.all()

    if category_id:
        services_list = services_list.filter(category_id=category_id)
    if query:
        services_list = services_list.filter(title__icontains=query)

    paginator = Paginator(services_list, 6)  # 6 послуг на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category_id': int(category_id) if category_id else None,
        'query': query or ''
    }
    return render(request, 'services.html', context)


# --- ДЕТАЛІ ПОСЛУГИ ---
def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug)
    # Розбиваємо етапи робіт по рядках, якщо вони записані через перенесення рядка
    stages_list = [stage.strip() for stage in service.stages.split('\n')] if service.stages else []

    context = {
        'service': service,
        'stages_list': stages_list
    }
    return render(request, 'service_detail.html', context)


# --- ВІДГУКИ ТА ДОДАВАННЯ ВІДГУКУ ---
def reviews_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rating = request.POST.get('rating', 5)
        object_info = request.POST.get('object_info', '')
        text = request.POST.get('text')

        # Зберігаємо відгук у базу
        Review.objects.create(
            name=name,
            rating=int(rating),
            object_info=object_info,
            text=text
        )

        # Миттєво сповіщаємо тебе в Telegram про новий відгук
        tg_msg = (
            f"⭐ *Новий відгук на сайті МартинБуд!* ⭐\n\n"
            f"👤 *Клієнт:* {name}\n"
            f"⭐ *Оцінка:* {rating}/5\n"
            f"🏢 *Об'єкт:* {object_info if object_info else 'Не вказано'}\n"
            f"💬 *Текст:* {text}"
        )
        send_telegram_notification(tg_msg)

        return redirect('reviews')

    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews})


# --- ГАЛЕРЕЯ ОБ'ЄКТІВ ---
def gallery_view(request):
    gallery_items = GalleryItem.objects.all()
    return render(request, 'gallery.html', {'gallery_items': gallery_items})


# --- ЧАСТІ ЗАПИТАННЯ (FAQ) ---
def faq_view(request):
    return render(request, 'faq.html')


# --- КОНТАКТИ ---
def contacts_view(request):
    return render(request, 'contacts.html')


# --- КАЛЬКУЛЯТОР ВАРТОСТІ ---
def calculator_view(request):
    return render(request, 'calculator.html')


# --- УНІВЕРСАЛЬНА ОБРОБКА ЗАЯВОК (працює і для contact, і для contacts, і для contact_us) ---
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment', request.POST.get('message', 'Без коментаря'))

        # Формуємо сповіщення в Telegram
        msg = (
            f"🚨 *УВАГА! Нова заявка з сайту МартинБуд!* 🚨\n\n"
            f"👤 *Ім'я:* {name}\n"
            f"📞 *Телефон:* `{phone}`\n"
            f"💬 *Повідомлення/Деталі:* {comment}"
        )

        # Надсилаємо миттєво в твій Telegram
        send_telegram_notification(msg)

        return redirect('home')

    return render(request, 'contact.html')