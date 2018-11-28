from django.core.exceptions import ValidationError


def validate_positive(value):
    if value < 0:
        raise ValidationError('Значение цены должно быть положительным!',
                              code='invalid')


def validate_price(cleaned_data):
    if cleaned_data.get('price', 0) < cleaned_data.get('old_price', 0):
        raise ValidationError('Цена с учетом скидки должна быть меньше!',
                              code='invalid')
