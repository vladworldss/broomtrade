from django import forms
from .models import Category, Good
from .validator import validate_positive, validate_price

NAME_ERROR_LIST = {'required': 'Укажите название товара',
                   'min_length': 'Слишком короткое название',
                   'max_length': 'Слишком длинное название'
                   }


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = '__all__'
        widgets = {'description': forms.Textarea, 'category': forms.RadioSelect}

    name = forms.CharField(label='Название', help_text='Должно быть уникальным',
                           error_messages=NAME_ERROR_LIST
                           )
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label=None,
        # widget=forms.RadioSelect
    )
    in_stock = forms.BooleanField(initial=True, label='Есть в наличии')
    price = forms.FloatField(label='Цена', validators=(validate_positive, ))

    def clean(self):
        cleaned_data = super().clean()
        validate_price(cleaned_data)
        return cleaned_data
