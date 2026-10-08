from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Категорія робіт")
    description = models.TextField(blank=True, null=True, verbose_name="Опис категорії")

    def __str__(self):
        return self.name


class WorkItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    title = models.CharField(max_length=200, verbose_name="Назва роботи (підкатегорія)")
    description = models.TextField(verbose_name="Детальний опис роботи")
    price = models.CharField(max_length=100, verbose_name="Орієнтовна ціна")
    # Місце для фотографії (зберігатиметься в папці media)
    image = models.ImageField(upload_to='works_photos/', blank=True, null=True, verbose_name="Фото роботи")

    def __str__(self):
        return f"{self.category.name} -> {self.title}"


class ContactRequest(models.Model):
    FULL_NAME_CHOICES = ...  # або просто текстове поле, як ти просив: ПІБ власними словами

    full_name = models.CharField(max_length=255, verbose_name="Прізвище, ім'я та по батькові")
    phone = models.CharField(max_length=50, verbose_name="Номер телефону")

    COMM_CHOICES = [
        ('phone', 'Дзвінок на номер телефону'),
        ('telegram', 'Telegram'),
        ('viber', 'Viber'),
        ('whatsapp', 'WhatsApp'),
    ]
    communication_method = models.CharField(max_length=20, choices=COMM_CHOICES, default='phone',
                                            verbose_name="Бажаний спосіб зв'язку")

    service_text = models.CharField(max_length=255, verbose_name="Бажана послуга (власними словами)")
    city = models.CharField(max_length=100, verbose_name="Населений пункт (місто/село)")
    object_type = models.CharField(max_length=100, verbose_name="Тип об'єкта (будинок, квартира тощо)")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар / деталі")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"Заявка від {self.full_name} ({self.phone}) - {self.city}"