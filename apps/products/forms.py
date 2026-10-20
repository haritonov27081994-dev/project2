from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Поля модели БАДа, которые будут в форме
        fields = ['title', 'price', 'description']
        
        # Настройка HTML-виджетов и подсказок (плейсхолдеров) как на уроке
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Например: Витамин С 1000мг (60 капсул)"
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': "0.00",
                'step': "0.01"
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Укажите дозировку, состав добавки и правила приема..."
            })
        }
        
        # Понятные названия полей на русском языке
        labels = {
            'title': 'Название товара',
            'price': 'Цена (руб)',
            'description': 'Описание и состав'
        }
        
    # Кастомная валидация названия (не менее 3 символов)
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Название должно содержать не менее 3 символов.')
        return title

    # Кастомная валидация цены (должна быть больше нуля)
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price
