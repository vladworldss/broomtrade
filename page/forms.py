from django import forms
from .models import Category, Good


NAME_ERROR_LIST = {'required': 'Укажите название товара',
                   'min_length': 'Слишком короткое название',
                   'max_length': 'Слишком длинное название'
                   }


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = '__all__'

    name = forms.CharField(label='Название', help_text='Должно быть уникальным',
                           error_messages=NAME_ERROR_LIST
                           )
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label=None
    )
    in_stock = forms.BooleanField(initial=True, label='Есть в наличии')

