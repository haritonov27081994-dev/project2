from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'manufacturer', 'price', 'image', 'description']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Например: Витамин С 1000мг (60 капсул)"
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': "0.00",
                'step': "0.01"
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Укажите дозировку, состав добавки и правила приема..."
            })
        }

        labels = {
            'title': 'Название товара',
            'category': 'Категория',
            'manufacturer': 'Производитель',
            'price': 'Цена (руб)',
            'image': 'Фотография товара',
            'description': 'Описание и состав'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Название должно содержать не менее 3 символов.')
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price
