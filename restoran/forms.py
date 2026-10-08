from django import forms
from .models import ContactRequest

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['full_name', 'phone', 'communication_method', 'service_text', 'city', 'object_type', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Мартин Назар Іванович'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380 ...'}),
            'communication_method': forms.Select(attrs={'class': 'form-control'}),
            'service_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: Монтаж даху'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'м. Новояворівськ / с. Шкло'}),
            'object_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Будинок, квартира тощо'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Додаткові побажання'}),
        }