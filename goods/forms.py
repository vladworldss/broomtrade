from django import forms

from goods.models import Good, Category


class GoodForm(forms.ModelForm):

  name = forms.CharField(label="Название")
  category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label=None)
  description = forms.CharField(label="Краткое описание", required=False)
  content = forms.CharField(label="Полное описание", required=False)
  price = forms.FloatField(label="Цена, руб.")
  price_acc = forms.FloatField(label="Цена с учетом скидки, руб.")
  in_stock = forms.BooleanField(label="Есть в наличии", required=False)
  featured = forms.BooleanField(label="Рекомендуемый", required=False)
  image = forms.ImageField(label="Основное изображение")

  class Meta:
    model = Good
    fields = '__all__'
