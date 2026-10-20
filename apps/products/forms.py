from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Указываем, какие поля модели должны быть в форме
        fields = ['title', 'price', 'description']
        
    # Добавляем кастомную валидацию для названия (не менее 3 символов)
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Название должно содержать не менее 3 символов.')
        return title

    # Добавляем кастомную валидацию для цены
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price
