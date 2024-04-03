import re

from django import forms

from config.models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '')
        description = cleaned_data.get('description', '')

        # Запрещенные слова
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        # Проверка наличия запрещенных слов
        for word in forbidden_words:
            # Преобразование к нижнему регистру и поиск совпадений
            if re.search(re.escape(word), name.casefold()):
                # Если найдено совпадение, вызываем исключение
                raise forms.ValidationError(f"Название содержит запрещенное слово: {word}")

            if re.search(re.escape(word), description.casefold()):
                raise forms.ValidationError(f"Описание содержит запрещенное слово: {word}")

        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current']
        labels = {
            'version_number': 'Номер версии',
            'version_name': 'Название версии',
            'is_current': 'Текущая версия'
        }

    # Задание стиля через инициализацию

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['version_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['version_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_current'].widget.attrs.update({'class': 'form-check-input'})
