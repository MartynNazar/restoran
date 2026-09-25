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